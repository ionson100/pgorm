import json
import uuid
import datetime
import psycopg2
import logging


from uuid import uuid4

from classTest import Test
from pgorm.orm import *



logging.basicConfig(level=logging.DEBUG)


# print(builder_attribute(name='date',
#                         default="null ",
#                         type='timestamp',
#                         is_pk=False))
# print(builder_attribute(name='age',
#                         default='0',
#                         type='integer'))
#
# from pgorm.orm import orm_int_connect, orm_exist_table, orm_create_table, orm_begin_transaction, orm_insert, orm_update, \
#     orm_select, orm_drop_table, orm_table_name, orm_column_name, orm_execute, orm_get_connect, getSession
#
print(ormInitConnect(password='postgres', host='192.168.70.119', port=5432, user='postgres', dbname='test'))






session=getSession()
exist=session.existTable(Test)
if exist:
    session.dropTable(Test)
    session.createTable(Test)
else:
    session.createTable(Test)

t = Test()
t.age = '45'
t.name = 'name'
session.insert(t)
t.name='name2'
session.update(t)
#res=session.execute("select * from test where age = %s",[45]);
res= session.select(Test,"where age = %s",(45))

for r in res:
    print(r)




