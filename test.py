import uuid
from uuid import uuid4


def builder_attribute(*,name:str,type:str,default:str,is_pk:bool=False):
   dec:dict[str,any()]= {'name': name, 'type': type, 'default': default, 'pk': is_pk}
   return dec

print(builder_attribute(name='id',
                        default="DEFAULT '00000000-0000-0000-0000-000000000000' ",
                        type='uuid',
                        is_pk=True))
print(builder_attribute(name='age',
                        default='0',
                        type='integer'))

from pgorm.orm import orm_int_connect, orm_exist_table, orm_create_table, orm_begin_transaction, orm_insert, orm_update, \
    orm_select

print(orm_int_connect(password='ion100312873', host='localhost', port=5432, user='postgres', dbname='test'))
class Test:
   """{'name':'test'}"""
   id:uuid
   """{'name': 'id', 'type': 'uuid', 'default': "DEFAULT '00000000-0000-0000-0000-000000000000' ", 'pk': True}"""
   mane:str
   """{'name':'name','type':'TEXT',  'default':'DEFAULT NULL'}"""
   age:int
   """{'name': 'age', 'type': 'integer', 'default': 'DEFAULT 0', 'pk': False}"""
print(orm_exist_table(Test))


#print(t.connection)
#print(orm_create_table(Test))
#t.commit()
c=uuid4().__str__()
t=Test()
t.id=c
t.age='45'
t.mane='qqq'
#orm_insert(t)
t.mane='ssssssssssssssssssssssss'
#orm_update(t)
orm_select(Test,"where age= (%s)",45)