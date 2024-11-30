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
Первый тип подключения:
```pycon
from pgorm.logAction import set_print
from pgorm.orm import OrmConnectionNotPool
#start app
OrmConnectionNotPool.init(password='postgres', host='localhost', port=5432, user='postgres', dbname='test')
# getting session
#contect context
with OrmConnectionNotPool.getSession(cursor_factory= psycopg2.extras.DictCursor) as session:
     print(session.executeQuery("select null"))
#or manual

session = OrmConnectionNotPool.getSession()
try:
      print(session.executeQuery("select null"))
finally:
      session.close()
```
Основная проблема была сделать механизм маппинга типа на таблицу в базе данных\
В питоне нет привычных атрибутов как в шарпе и джаве, что бы пометить свойство и на основе этого сделать\
маппинг на талицу базы данных.\
Да и само определение свойства многословно, что бы использовать декораторы
Решил попробовать через строку документа поля и типа (описание)
И так пример: будем работать в двумя таблицами
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
Вот тип, который проецируется в таблицу с названием: myUser
три колонки, строка запроса на создание:
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
Давайте наследуемся и создадим две таблицы, с одинаковой структурой, но с разным типом генерации первичного ключа.
```python
from uuid import uuid4
from pgorm import set_print
from pgorm import OrmConnectionNotPool

OrmConnectionNotPool.init(password='ion100312873', host='localhost', port=5432, user='postgres', dbname='test')
set_print(True) # говорит что нужно печатать все запросы в консоль
class UserBase:
    name: str=''
    """orm{'name': 'name', 'type': 'text', 'default': 'DEFAULT NULL'}orm"""

    age: int=10
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
Вставка в базу данных (генерация ключа на клиенте).
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
Вставка в базу данных (генерация ключа на сервере).
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
Получение содержимого таблицы по типу:
```python
        for u in session.select(UserDatabase):
            print(u)
        """
        генератор на основе yield, возвращает итератор объектов заданного тира
        Запрос выглядит
        ORM SESSION: select:('SELECT "id", "name", "age" FROM "myUser2" ;', []) 
        """
```
с параметрами:
```python
        for u in session.select(UserDatabase, 'where age = %(age)s and name <> %(name)s ',{'age':10,'name':'simple'}):
            print(u)
        """
        генератор на основе yield, возвращает итератор объектов заданного тира
        Запрос выглядит
        ORM SESSION: select:('SELECT "id", "name", "age" FROM "myUser2" where age = %(age)s and name <> %(name)s;', {'age': 10, 'name': 'simple'}) 
        """
```
Получение массивом:
```python
        for u in session.selectList(UserDatabase, 'where age = %s and name <> %s ',(10,'simple')):
            print(u)
        """
        Если результат пустой, вернется массив нулевой длины
        Запрос выглядит
        ORM SESSION: selectList:('SELECT "id", "name", "age" FROM "myUser2" where age = %s and name <> %s;', (10, 'simple')) 
        """
```
Получение объекта по первичному ключу:
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
Построение строки запроса:
Бываю случаи кода название таблицы в базе не совпадает с названием типа, или название поля\
не совпадает с названим колонки таблицы, или в процессе проектирования вы поменяли что-то. \
Стоит применять такие методы.
```python
        print(f"SELECT * FROM {tableName(UserDatabase)} where {columnName(UserDatabase,"age")} =10 ")
        """ получение названия таблицы м колонки таблицыSELECT * FROM "myUser2" where "age" =10 """
        print(getSqlForType(UserDatabase))
        """ получение канонической строки  запроса -SELECT "id", "name", "age" FROM "myUser2" """
```
Выборка со свободным запросом:
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

