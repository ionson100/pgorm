from dataclasses import dataclass
from uuid import uuid4

import pgorm
from pgorm import set_print, Session, tableName, columnName, getSqlForType, getTemplateTableAttributesDoc
from pgorm import OrmConnectionNotPool
from pgorm import OrmConnectionPool
from test import connect

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

@dataclass
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


OrmConnectionPool.init(type_pool=0,minconn=1,maxconn=10,password='postgres', host='localhost', port=5432, user='postgres1', database='test',)
with OrmConnectionPool.getContext() as ctx:
    with OrmConnectionPool.getConnection() as connection:
        with connection.getSession() as session:
            with session.beginTransaction() as tx:
                session.dropTable(UserDatabase, True)
                session.createTable(UserDatabase, True)
                session.truncateTable(UserDatabase)



# в ручном режиме
OrmConnectionPool.init(type_pool=0,minconn=1,maxconn=10,password='postgres', host='localhost', port=5432, user='postgres1', database='test',)
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
print(getTemplateTableAttributesDoc(name="my_name",type_column="TEXT",default=" null",pk=False,mode=False))
"""
orm{'name': 'my_name', 'type': 'TEXT', 'default': ' null', 'pk': False, 'mode': False}orm
"""


