import logging
from models.classTest22 import Test221
from pgorm.orm import OrmConnection

logging.basicConfig(level=logging.DEBUG)

with OrmConnection(password='postgres', host='192.168.70.119', port=5432, user='postgres', dbname='test') as c:
    with OrmConnection.getSession() as session:
        exist = session.existTable(Test221)
        if exist:

            session.dropTable(Test221)
            session.createTable(Test221)
        else:
            session.createTable(Test221)
        session.deleteFromOnlyTable(Test221)
        session.insert(Test221())
        # transaction=session.beginTransaction();
        session.insertBulk([Test221('bulk1'), Test221('bulk2')])
        # transaction.commit()
        # session.insertBulk([Test221('tx1'), Test221('tx2')])
        res = session.select(Test221)
        for r in res:
            print(r)
