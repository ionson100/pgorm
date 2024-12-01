


from models.classTest221 import Test221
from pgorm import columnName, tableName
from pgorm.ormPool import OrmConnectionPool
from pgorm.logAction import set_print




OrmConnectionPool.init(type_pool=0, minconn=1, maxconn=10,
                       user='postgres1', password='postgres', host='localhost', port=5432, database='test')
set_print(True)
#
with OrmConnectionPool.getConnection()as connect:
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


            res = session.execute(f'select {columnName(Test221,"id")} from {tableName(Test221)}')
            for r in res:
                print(r)
print('*******************************************************************************************')
with OrmConnectionPool.getConnection()as connect:
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


            res = session.execute(f'select {columnName(Test221,"id")} from {tableName(Test221)}')
            for r in res:
                print(r)




