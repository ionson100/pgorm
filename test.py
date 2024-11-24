import json
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
    orm_select, orm_drop_table, orm_table_name, orm_column_name

print(orm_int_connect(password='ion100312873', host='localhost', port=5432, user='postgres', dbname='test'))


class Test:
    """
    Тестовый класс\n
    orm{'name':'test'}orm
    """

    id: uuid=uuid4().__str__()
    """
    Эта переменная тестовая\n
    orm{
    'name': 'id',
    'type': 'uuid',
    'default': "DEFAULT '00000000-0000-0000-0000-000000000000' ",
    'pk': True
    }orm
    
    """
    name2:str='sdsd'
    """
    sasasi isoais i
    """
    def __str__(self):
        """
        saaspaos osapospaos
        :return:
        """
        return self.id
    name: str
    """orm{'name':'name','type':'TEXT',  'default':'DEFAULT NULL'}orm"""
    age: int
    """orm{'name': 'age', 'type': 'integer', 'default': 'DEFAULT 0'}orm"""

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __json__(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)





# if orm_exist_table(Test):
#     orm_drop_table(Test)
#     orm_create_table(Test)
# else:
#     orm_create_table(Test)





t = Test()
t.age = '45'
t.name = 'qqq'
orm_insert(t)
# t.name = 'ssssssssssssssssssssssss'
# orm_update(t)
res=orm_select(Test, "where age= (%s)", 45)
for r in res:
    c=r.name2
    print(c)
    print(r.__json__())
print(orm_table_name(Test))
print(orm_column_name(Test,"name"))