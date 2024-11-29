import logging
from uuid import uuid4

from models.classForeignKey import ForeignKey
from models.classTest221 import Test221
from pgorm import Session
from pgorm.orm import OrmConnectionNotPool

logging.basicConfig(level=logging.DEBUG)

with OrmConnectionNotPool(password='postgres', host='192.168.70.119', port=5432, user='postgres', dbname='test') as c:
    with OrmConnectionNotPool.getSession() as session:

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
        session.truncateTable(Test221)
        session.tableName(ForeignKey)

        t=Test221()
        session.insert(t)

        t_fk=ForeignKey()
        t_fk.id_test=t.id


        t_fk2 = ForeignKey()
        t_fk2.id_test = t.id
        session.insertBulk([t_fk,t_fk2])


        res = session.select(Test221)
        for r in res:
            print(r.getForeignObject())
            print(r.getForeignObject())
        # print(session.get(Test221,t.id))
        # print(session.get(Test221, str(uuid4())))
        #print(session.firstOrNull(Test221,f'where {Session.columnName(Test221,'name')} = %s',[t.name]))

        #print(session.singleOrException(Test221,f'where {Session.columnName(Test221,'id')} = %s',[str(uuid4())]))
        print(session.deleteFromTable(Test221,f'where {Session.columnName(Test221,'id')} = %s ; ',[str(uuid4())]))