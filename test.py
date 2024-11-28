


import logging
from models.classTest22 import Test221
from pgorm.orm import OrmConnection

logging.basicConfig(level=logging.DEBUG)



with OrmConnection(password='postgres', host='192.168.70.119', port=5432, user='postgres', dbname='test') as c:
    with OrmConnection.getSession() as session:
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
            raise Exception('sdsdsd')

            res = session.execute(f"select {session.columnName(Test221,"id")} from {session.tableName(Test221)}")
            for r in res:
                print(r)


