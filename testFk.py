import logging

from models.classForeignKey import ForeignKey
from models.classTest221 import Test221
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

        exist1 = session.existTable(ForeignKey)
        if exist1:
            session.dropTable(ForeignKey)
            session.createTable(ForeignKey)
        else:
            session.createTable(ForeignKey)

        t=Test221()
        t_fk=ForeignKey();
        t_fk.id_test=t.id
        session.insert(t)
        session.insert(t_fk)


        res = session.select(Test221)
        for r in res:
            print(r.getForeignObject())