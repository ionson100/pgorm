from uuid import uuid4

import pgorm
from pgorm import set_print, Session, tableName, columnName, getSqlForType
from pgorm import OrmConnectionNotPool

OrmConnectionNotPool.init(password='ion100312873', host='localhost', port=5432, user='postgres', dbname='test')
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
    первичный ключ генерим на клиенте
    orm{'name': 'id','type': 'SERIAL','default': "PRIMARY KEY",'pk': True,'mode':True}orm
     """

    def __init__(self, name: str = 'user'):
        self.name = name

    def __str__(self):
        return f'{self.id} {self.name} {self.age}'


with OrmConnectionNotPool.getSession() as session:
    with session.beginTransaction() as tx:
        session.dropTable(UserClient, True)
        session.createTable(UserClient, True)

        session.dropTable(UserDatabase, True)
        session.createTable(UserDatabase, True)

        user = UserDatabase()
        user.name = '<NAME>'
        session.insert(user)

        print(f"SELECT * FROM {tableName(UserDatabase)} where {columnName(UserDatabase, "age")} =10 ")
        """ получение названия таблицы м колонки таблицыSELECT * FROM "myUser2" where "age" =10 """
        print(getSqlForType(UserDatabase))
        """ получение канонической строки  запроса -SELECT "id", "name", "age" FROM "myUser2" """
        for r in session.execute(getSqlForType(UserDatabase)):
            print(r)

        for r in session.execute(f' {getSqlForType(UserDatabase)}  where {columnName(UserDatabase, "age")} =%s;', [10]):
            print(r)

        """
        execute возвращает генератор кортежей строк запроса.
        ORM SESSION: execute:('SELECT "id", "name", "age" FROM "myUser2" ', None)
        ORM SESSION: execute:(' SELECT "id", "name", "age" FROM "myUser2"   where "age" =%s;', [10]) 
        """


        # li=[]
        # for  i in range(2):
        #     user = UserClient()
        #     user.name = 'name-'+str(i)
        #     #user.age=10
        #     li.append(user)
        # session.insertBulk(li)
        # for u in session.select(UserClient):
        #     print(u)
