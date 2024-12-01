Микро орм обертка для psycopg2 Postgres\
https://www.psycopg.org/docs/ \
выполнена в стиле Hibernate. Дает возможность работать с базой на уровне объектов.\
Схема работы:\
При старте программы открываете перманентное соединение с базой. Одно на все приложение.\
Из любого модуля обращаетесь к соединению и получаете легкий объект сессии\
Из сессии выполняете запросы.\
По окончанию работы закрываете сессию, или в ручную, или через контекст.\
Второй вариант. При старте приложения вы открываете пул соединений, \
где указываете минимальное и максимальное количество соединений, тип пула:\
0 - SimpleConnectionPool\
другое - ThreadedConnectionPool\
Из любого модуля подключаетесь к пулу, получаете сессию, работаете с базой\
по окончанию работы, закрываете сессию, возвращаете соединение в пул.
Первый тип подключения работа без пула:
```pycon
from pgorm.logAction import set_print
from pgorm.orm import OrmConnectionNotPool
#start app
OrmConnectionNotPool.init(password='postgres', host='localhost', port=5432, user='postgres', dbname='test')
# getting session
#contect context
with OrmConnectionNotPool.getContext() as ctx:
    with OrmConnectionNotPool.getSession() as session:
#or manual

session = OrmConnectionNotPool.getSession()
try:
      print(session.executeQuery("select null"))
finally:
      session.close()
      OrmConnectionNotPool.connectionClose()
     
```
работа с пулом:
```python
OrmConnectionPool.init(type_pool=0,minconn=1,maxconn=10,password='postgres', host='localhost', port=5432, user='postgres', database='test',)
with OrmConnectionPool.getContext() as ctx:
    with OrmConnectionPool.getConnection() as connection:
        with connection.getSession() as session:
            with session.beginTransaction() as tx:
                session.dropTable(UserDatabase, True)
                session.createTable(UserDatabase, True)
                session.truncateTable(UserDatabase)



# в ручном режиме
OrmConnectionPool.init(type_pool=0,minconn=1,maxconn=10,password='postgres', host='localhost', port=5432, user='postgres', database='test',)
connect=OrmConnectionPool.getConnection()
session=connect.getSession()
try:
    session.dropTable(UserDatabase, True)
except Exception as e:
    print(e)
    raise
finally:
    session.close()
    connect.close()
    OrmConnectionPool.ClosePool()
```

Основная проблема была сделать механизм маппинга типа на таблицу в базе данных\
В питоне нет привычных атрибутов как в шарпе и джаве, что бы пометить свойство и на основе этого сделать\
маппинг на талицу базы данных.\
Да и само определение свойства многословно, что бы использовать декораторы\
Решил попробовать через строку документа поля и типа (описание)\
И так пример: будем работать в двумя таблицами\
```pycon
class User:
    """
    orm{'name':'myUser'}orm
    таблица пользователей
    """
    id: str
    """
    первичный ключ uuid as string
    orm{'name': 'id','type': 'uuid','default': "PRIMARY KEY' ",'pk': True,'mode':False}orm
     """

    name: str=''
    """orm{'name': 'name', 'type': 'text', 'default': 'DEFAULT NULL'}orm"""

    age: int=10
    """
    возраст пользователя
    orm{'name': 'age', 'type': 'integer', 'default': 'DEFAULT 10'}orm
    """

    def __init__(self, name):
        self.id = str(uuid4())
        self.name = name

    def __str__(self):
        return f'{self.__class__.__name__}({self.name})'
```
Вот тип, который проецируется в таблицу с названием: myUser\
три колонки, строка запроса на создание:\



```sql
CREATE TABLE IF NOT EXISTS  "myUser" (
    "id" uuid  DEFAULT PRIMARY KEY ,
   "name" text DEFAULT 10,
   "age" integer null
);
```
обратите внимание на ключь mode в описании первичного ключа.\
False - это означает что мы генерим уникальность на клиенте, а не в базе,
True - база данных сама генерит уникальный ключ\

для облегчения создания строки описания можно применить функцию:
```python

  print(getTemplateTableAttributesDoc(name="my_name",type_column="TEXT",default=" null",pk=False,mode=False))
  """
  orm{'name': 'my_name', 'type': 'TEXT', 'default': ' null', 'pk': False, 'mode': False}orm
  """
```
Давайте наследуемся и создадим две таблицы, с одинаковой структурой, но с разным типом генерации первичного ключа.

```python
from uuid import uuid4
from pgorm import set_print
from pgorm import OrmConnectionNotPool


set_print(True)  # говорит что нужно печатать все запросы в консоль


class UserBase:
    name: str = ''
    """orm{'name': 'name', 'type': 'text', 'default': 'DEFAULT NULL'}orm"""

    age: int = 10
    """
    возраст пользователя
    orm{'name': 'age', 'type': 'integer', 'default': 'DEFAULT 10'}orm
    """


class UserClient(UserBase):
    """
    orm{'name':'myUser1'}orm
    таблица пользователей
    """
    id: str
    """
    первичный ключ генерим на клиенте
    orm{'name': 'id','type': 'uuid PRIMARY KEY','default': "DEFAULT '00000000-0000-0000-0000-000000000000' ",'pk': True,'mode':False}orm
     """

    def __init__(self):
        self.id = str(uuid4())

    def __str__(self):
        return f'{self.id} {self.name} {self.age}'


class UserDatabase(UserBase):
    """
    orm{'name':'myUser2'}orm
    таблица пользователей
    """
    id: int
    """
    первичный ключ генерим в базе данных
    orm{'name': 'id','type': 'SERIAL','default': "PRIMARY KEY",'pk': True,'mode':True}orm
     """

    def __init__(self):
        pass

    def __str__(self):
        return f'{self.id} {self.name} {self.age}'
# РАБОТА С ПУЛОМ
#OrmConnectionPool.init(type_pool=0,minconn=1,maxconn=10,password='postgres', host='localhost', port=5432, user='postgres', database='test',)
# with OrmConnectionPool.getContext() as ctx:
#     with OrmConnectionPool.getConnection() as connection:
#         with connection.getSession() as session:
#             with session.beginTransaction() as tx:
#                 session.dropTable(UserDatabase, True)
#                 session.createTable(UserDatabase, True)
#                 session.truncateTable(UserDatabase)

#РФБОТА БЕЗ ПУЛА
OrmConnectionNotPool.init(password='postgres', host='localhost', port=5432, user='postgres', dbname='test')
with OrmConnectionNotPool.getContext() as ctx:
    with OrmConnectionNotPool.getSession() as session:
        with session.beginTransaction() as tx:
            session.dropTable(UserClient, True)
            session.createTable(UserClient, True)

            session.dropTable(UserDatabase, True)
            session.createTable(UserDatabase, True)
```
Обратите внимание, орм отсылает None в базу данных ели поле не инициализировано.\
По это му стоить следить за значениями по умолчанию. \
Важно заметить, что соединение настроено на autocommit=True, \
по этому работа с трансакциями выглядит так:
```python
with OrmConnectionNotPool.getSession() as session:

    with session.beginTransaction() as tx:
        session.dropTable(UserClient, True)
        session.createTable(UserClient, True)

        session.dropTable(UserDatabase, True)
        session.createTable(UserDatabase, True)
```
или так
```python
    transaction=session.beginTransaction()
    try:
        session.dropTable(UserClient, True)
        session.createTable(UserClient, True)

        session.dropTable(UserDatabase, True)
        session.createTable(UserDatabase, True)
        transaction.commit()
    except Exception as e:
        transaction.rollback()
        raise
```
#### Вставка в базу данных (генерация ключа на клиенте).
```python

        user=UserClient()
        user.name='<NAME>'
        session.insert(user)
        #получение содержимого таблицы
        for u in session.select(UserClient):
            print(u)
        """
        Запрос выглядит
        ORM SESSION: insert.sql:('INSERT INTO "myUser1" ("id", "name", "age") VALUES ((%s), (%s), (%s)) ;', ['254f2346-28ee-4467-a6a7-ab3064dc82ea', '<NAME>', 10])
        """
```
#### Вставка в базу данных (генерация ключа на сервере).
```python
        user=UserDatabase()
        user.name='<NAME>'
        session.insert(user)
        #получение содержимого таблицы
        for u in session.select(UserDatabase):
            print(u)
        """
        Запрос выглядит
        ORM SESSION: insert.sql:('INSERT INTO "myUser2" ("name", "age") VALUES ((%s), (%s)) RETURNING "id" ;', ['<NAME>', 10]) 
        я не отсылаю ключ на сервер, в коне запроса, я прошу вернуть сгенеренный ключ, и вставляю в объект, который я отослал для вставки
        """
```
#### Вставка пакетом:
Для вставки передается массив, 
внимание, все объекты в массиве должны быть одного типа, и помеченны птсанием для проекции в базе данных:
```python
        li:list[UserDatabase]=[]
        for  i in range(2):
            user = UserDatabase()
            user.name = 'name-'+str(i)
            li.append(user)
        session.insertBulk(li)
        for u in session.select(UserDatabase):
            print(u)
            """
            ORM SESSION: insertBulk:('INSERT INTO "myUser2" ("name", "age") VALUES (%s, %s), (%s, %s) RETURNING "id" ;', ['name-0', 10, 'name-1', 10]) 
            """
```







#### Получение содержимого таблицы по типу:
```python
        for u in session.select(UserDatabase):
            print(u)
        """
        генератор на основе yield, возвращает итератор объектов заданного типа
        Запрос выглядит
        ORM SESSION: select:('SELECT "id", "name", "age" FROM "myUser2" ;', []) 
        """
```
#### с параметрами:
```python
        for u in session.select(UserDatabase, 'where age = %(age)s and name <> %(name)s ',{'age':10,'name':'simple'}):
            print(u)
        """
        генератор на основе yield, возвращает итератор объектов заданного тира
        Запрос выглядит
        ORM SESSION: select:('SELECT "id", "name", "age" FROM "myUser2" where age = %(age)s and name <> %(name)s;', {'age': 10, 'name': 'simple'}) 
        """
```
#### Получение массивом:
```python
        for u in session.selectList(UserDatabase, 'where age = %s and name <> %s ',(10,'simple')):
            print(u)
        """
        Если результат пустой, вернется массив нулевой длины
        Запрос выглядит
        ORM SESSION: selectList:('SELECT "id", "name", "age" FROM "myUser2" where age = %s and name <> %s;', (10, 'simple')) 
        """
```
#### Получение объекта по первичному ключу:
```python
        user=UserDatabase()
        user.name='<NAME>'
        session.insert(user)

        print(session.getByPrimaryKey(UserDatabase,user.id))
        """
        Запрос выглядит
        ORM SESSION: getByPrimaryKey:SELECT "id", "name", "age" FROM "myUser2" WHERE "id" = %s, [1] 
        """
```
#### Получение только первого элемента в наборе или ничего:
```python
            print(session.firstOrNull(UserDatabase,"where id =%s",[user.id]))
            """
            execute возвращает объект типа  или если ничего не найдено None.
            ORM SESSION: firstOrNull:('SELECT "id", "name", "age" FROM "myUser2" where id =%s LIMIT 1;', [1]) 
            """
```
#### Получение единичного елемента, если ничего не найдено выкидывается исключение:
```python
            print(session.singleOrException(UserDatabase,"where id =%s",[user.id]))
            """
            ORM SESSION: singleOrException:('SELECT "id", "name", "age" FROM "myUser2" where id =%s;', [1]) 
            """
```










#### Построение строки запроса:
Бываю случаи кода название таблицы в базе не совпадает с названием типа, или название поля\
не совпадает с названим колонки таблицы, или в процессе проектирования вы поменяли что-то. \
Стоит применять такие приемы.
```python
        print(f"SELECT * FROM {tableName(UserDatabase)} where {columnName(UserDatabase,"age")} =10 ")
        """ получение названия таблицы м колонки таблицыSELECT * FROM "myUser2" where "age" =10 """
        print(getSqlForType(UserDatabase))
        """ получение канонической строки  запроса -SELECT "id", "name", "age" FROM "myUser2" """
```
#### Выборка со свободным запросом:
```python
        for r in session.execute(getSqlForType(UserDatabase)):
            print(r)

        for r in session.execute(f' {getSqlForType(UserDatabase)}  where {columnName(UserDatabase, "age")} =%s;', [10]):
            print(r)

        """
        execute возвращает генератор кортежей строк запроса.
        ORM SESSION: execute:('SELECT "id", "name", "age" FROM "myUser2" ', None)
        ORM SESSION: execute:(' SELECT "id", "name", "age" FROM "myUser2"   where "age" =%s;', [10]) 
        """
```
```python
        session.executeNonQuery('SET statement_timeout = %s; ',[6000])
        print(session.executeQuery("show statement_timeout;"))
        """
        executeNonQuery возвращает количество затронутых строк
        executeQuery возвращает массив кортежей строк
        ORM SESSION: executeNotQuery:('SET statement_timeout = %s; ', [6000]) 
        ORM SESSION: executeNotQuery:('show statement_timeout;', None) 
        [('6s',)] 
        """
```
#### Проверка на существование таблицы:
```python
        print(session.existTable(UserDatabase))
        """
        ORM SESSION: existTable:SELECT EXISTS  ( SELECT FROM  pg_tables WHERE  schemaname = 'public' AND  tablename  = 'myUser2' ); 
        True
        """
```
#### Создание таблицы:
```python
        session.createTable(UserDatabase, True)
            """
            параметр add_exist = True добавляет с строку запроса  IF NOT EXISTS
            ORM SESSION: createTable :
            CREATE TABLE IF NOT EXISTS  "myUser2" (
            "id" SERIAL  PRIMARY KEY,
            "name" text DEFAULT NULL,
            "age" integer DEFAULT 10
             ); 
            """
```
#### Удаление таблицы:
```python
         session.dropTable(UserDatabase, True)
            """
            параметр add_exist = True добавляет с строку запроса  IF EXISTS
            ORM SESSION: drop table:DROP TABLE IF EXISTS "myUser2"; 
            """
```
#### Очистка таблицы:
```python
        session.deleteFromTable(UserDatabase,'where age > %s',[10])
            """
            Очистка таблицы, с связанных записей в других таблицах
            ORM SESSION: delete table.sql:DELETE FROM "myUser2" where age > %s; [10] 
            """
```
```python
       session.deleteFromOnlyTable(UserDatabase,'where age > %s',[10])
        """
        Очистка таблицы только указанной таблицы
        ORM SESSION: delete table.sql:DELETE FROM "myUser2" where age > %s; [10] 
        """
```
#### Проверка на существование записей в таблице:
```python
       print(session.any(UserDatabase,'where age = %s',[10]))
        """
        ORM SESSION: any:('SELECT EXISTS (SELECT 1 FROM "myUser2" where age = %s);', [10]) 
        False
        """
```
#### Очистка таблицы, путоём пересоздания:
```python
       session.truncateTable(UserDatabase)
        """
        ORM SESSION: truncateTable:TRUNCATE TABLE  "myUser2"; 
        """
```
#### Работа с json
пример:
```python
import datetime
import json


from pgorm import OrmConnectionPool, set_print
set_print(True)

class Inner:
    def __init__(self):
        self.name='sd'
        self.age=22

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
class TestJson:
    """orm{'name':'json'}orm"""
    id: int
    """
    первичный ключ генерим на клиенте
    orm{'name': 'id','type': 'SERIAL','default': "PRIMARY KEY",'pk': True,'mode':True}orm
     """
    array=[1,2,3,4]
    """orm{'name': 'array','type': 'integer[]','default': "null"}orm"""


    dict={'name':'name','age':34}
    """orm{'name': 'dict','type': 'jsonb','default': "null"}orm"""

    inner=Inner()
    """orm{'name': 'inner','type': 'jsonb','default': "null"}orm"""

    my_date=datetime.date.today()
    """orm{'name': 'date','type': 'timestamp','default': "null"}orm"""
    def __str__(self):
       return f'id-{self.id}, array-{self.array}, dict-{self.dict}, my_date-{self.my_date}, inner-{self.inner}'



OrmConnectionPool.init(type_pool=0,minconn=1,maxconn=10,password='postgres', host='localhost', port=5432, user='postgres1', database='test',)
with OrmConnectionPool.getContext() as ctx:
    with OrmConnectionPool.getConnection() as connection:
        with connection.getSession() as session:
            with session.beginTransaction() as tx:
              session.dropTable(TestJson,True)
              session.createTable(TestJson,True)
              session.insert(TestJson())
              for r in session.select(TestJson):
                  print(r)
"""
ORM SESSION: insert:('INSERT INTO "json" ("array", "dict", "inner", "date") VALUES ((%s), (%s), (%s), (%s)) RETURNING "id" ;', [[1, 2, 3, 4], '{"name": "name", "age": 34}', '{"name": "sd", "age": 22}', datetime.date(2024, 12, 1)]) 
ORM SESSION: select:('SELECT "id", "array", "dict", "inner", "date" FROM "json" ;', None) 
id-1, array-[1, 2, 3, 4], dict-{'age': 34, 'name': 'name'}, my_date-2024-12-01 00:00:00, inner-{'age': 22, 'name': 'sd'}
"""
```
орм умеет посылать, объекты в виде json на хранение в базу данных в тип поля jdonb\
c примитивными типами родной конвертор справляется легко, а кастомными не может, \
по этому ваш тип должен реализовывать метод toJson который возвращает строку json.
еще минус, при вытаскивании из базы, ваши кастомные объекты превращаются в словарь, \
по этому если вы захотите работать с полноценными объектами, вам придется сделать фабрику\
переделки словаря в объект, ну имх не сложно.

#### Резюме:
Библиотека создана на python 3.12, psycopg2-binary==2.9.10\
ниже 3.10 работать не будет\
одно соединение или одни пул на весь главный поток программы (к нодам не относится)
все модели должны иметь один первичный ключ \
при инициализации модели конструктор не должен иметь обязательных параметров\
декоратор dataclass уместен. \
для вывода запросов в консоль:
```python
set_print(True) 
```


