import uuid
from msilib import Table
from uuid import uuid4


def builder_attribute(*, name: str, type: str, default: str, is_pk: bool = False):
    dec: dict[str, any()] = {'name': name, 'type': type, 'default': default, 'pk': is_pk}
    return dec


print(builder_attribute(name='id',
                        default="DEFAULT {} '00000000-0000-0000-0000-000000000000' ",
                        type='uuid',
                        is_pk=True))
print(builder_attribute(name='age',
                        default='0',
                        type='integer'))

from pgorm.orm import orm_int_connect, orm_exist_table, orm_create_table, orm_begin_transaction, orm_insert, orm_update, \
    orm_select, orm_drop_table

print(orm_int_connect(password='ion100312873', host='localhost', port=5432, user='postgres', dbname='test'))


class Test:
    """orm{'name':'test'}orm"""

    id: uuid
    """
    Эта переменная тестовая\n
    orm{
    'name': 'id',
    'type': 'uuid',
    'default': "DEFAULT '00000000-0000-0000-0000-000000000000' ",
    'pk': True
    }orm
    
    """
    mane: str
    """orm{'name':'name','type':'TEXT',  'default':'DEFAULT NULL'}orm"""
    age: int
    """orm{'name': 'age', 'type': 'integer', 'default': 'DEFAULT 0'}orm"""



if orm_exist_table(Test):
    orm_drop_table(Test)
    orm_create_table(Test)
else:
    orm_create_table(Test)




c = uuid4().__str__()
t = Test()
t.id = c
t.age = '45'
t.mane = 'qqq'
orm_insert(t)
t.mane = 'ssssssssssssssssssssssss'
orm_update(t)
orm_select(Test, "where age= (%s)", 45)
