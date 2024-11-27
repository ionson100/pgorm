

import psycopg2
import logging
from classTest import Test
from pgorm.orm import OrmConnection
from pgorm.session import Session
import uuid

#logging.basicConfig(level=logging.DEBUG)

t = OrmConnection.getTemplateTableAttributesDoc(name='id', default="0000-00-00 00:00:00", typeColumn='uuid')
print(t)

with OrmConnection(password='ion100312873', host='localhost', port=5432, user='postgres', dbname='test') as c:
    with OrmConnection.getSession() as session:
        with session.beginTransaction() as tx:
            exist = session.existTable(Test)
            # if exist:
            #     session.dropTable(Test)
            #     session.createTable(Test)
            # else:
            #     session.createTable(Test)

            # t = Test()
            # t.id=uuid.uuid4().__str__()
            # t.name = 'name'
            #
            # tt = Test()
            # tt.id = uuid.uuid4().__str__()
            # tt.name = 'name'
            #
            #
            # session.insertBulk([t,tt])
            # # session.insert(t)
            # # t.name = 'name2'
            # # session.update(t)
            #session.truncateTable(Test)
            session.deleteFromOnlyTable(Test,'where age = %(assa)s',{"assa":23})
            l=[]
            for u in range(2):
                f=Test()
                f.name=str(u)+'name'+str(u)
                l.append(f)
            session.insertBulk(l)

            res1=session.execute(f"select {Session.columnName(Test,'id')} from {Session.tableName(Test)} ")
            for r in res1:
                print(r)
            res = session.select(Test)
            for r in res:
                print(r)

