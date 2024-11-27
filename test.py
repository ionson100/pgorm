

import psycopg
import logging
from classTest import Test
from pgorm.orm import OrmConnection
from pgorm.session import Session
import uuid

#logging.basicConfig(level=logging.DEBUG)

t = OrmConnection.getTemplateTableAttributesDoc(name='id', default="0000-00-00 00:00:00", typeColumn='uuid')
print(t)
# - *dbname*: the database name
#     - *database*: the database name (only as keyword argument)
#     - *user*: user name used to authenticate
#     - *password*: password used to authenticate
#     - *host*: database host address (defaults to UNIX socket if not provided)
#     - *port*: connection port number (defaults to 5432 if not provided)
with OrmConnection(password='ion100312873', host='localhost', port=5432, user='postgres', dbname='test') as c:
    with OrmConnection.getSession() as session:
        with session.beginTransaction() as tx:
            exist = session.existTable(Test)
            if exist:
                session.dropTable(Test)
                session.createTable(Test)
            else:
                session.createTable(Test)

            print(session.insert(Test()))
            #raise Exception(sd)
            # t1=session.beginTransaction()
            # print(session.insert(Test()))
            # t1.rollback()


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
            # session.deleteFromOnlyTable(Test,'where age = %(assa)s',{"assa":23})
            # l=[]
            # for u in range(10):
            #     f=Test()
            #     f.name=str(u)+'name'+str(u)
            #     l.append(f)
            # session.insertBulk(l)

            # res1=session.execute(f"select {Session.columnName(Test,'id')} from {Session.tableName(Test)} ")
            # for r in res1:
            #     print(r)
            res = session.select(Test)

            # session.existTable(Test)
            for r in res:
                print(r)

