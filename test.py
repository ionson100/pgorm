
import logging

from pgorm.orm import OrmConnectionNotPool
from models.classTest221 import Test221
from pgorm.ormPool import OrmConnectionPool

logging.basicConfig(level=logging.DEBUG)

OrmConnectionPool.init(type_pool=0, minconn=1, maxconn=10,
                       user='postgres', password='ion100312873', host='localhost', port=5432, database='test')
#
with OrmConnectionPool.GetConnection()as connect:
   with connect.getSession() as session:
        with session.beginTransaction() as tx:
            exist = session.existTable(Test221)
            if exist:
                session.dropTable(Test221)
                session.createTable(Test221)
            else:
                session.createTable(Test221)

            session.insert(Test221())
            session.cancel()
            session.insertBulk([Test221('bulk1'),Test221('bulk2')])


            res = session.execute(f'select {session.columnName(Test221,"id")} from {session.tableName(Test221)}')
            for r in res:
                print(r)
print('*******************************************************************************************')
with OrmConnectionPool.GetConnection()as connect:
   with connect.getSession() as session:
        with session.beginTransaction() as tx:
            exist = session.existTable(Test221)
            if exist:
                session.dropTable(Test221)
                session.createTable(Test221)
            else:
                session.createTable(Test221)

            session.insert(Test221())
            session.cancel()
            session.insertBulk([Test221('bulk1'),Test221('bulk2')])


            res = session.execute(f'select {session.columnName(Test221,"id")} from {session.tableName(Test221)}')
            for r in res:
                print(r)




