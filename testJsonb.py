import datetime
import json


from pgorm import OrmConnectionPool, set_print, MapBuilder

set_print(True)

class Inner:
    def __init__(self):
        self.name='sd'
        self.age=22

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
class TestJson:
    # """orm{'name':'json'}orm"""
    id: int
    # """
    # первичный ключ генерим на клиенте
    # orm{'name': 'id','type': 'SERIAL','default': "PRIMARY KEY",'pk': True,'mode':True}orm
    #  """
    array=[1,2,3,4]
    # """orm{'name': 'array','type': 'integer[]','default': "null"}orm"""


    dict={'name':'name','age':34}
    # """orm{'name': 'dict','type': 'jsonb','default': "null"}orm"""

    inner=Inner()
    # """orm{'name': 'inner','type': 'jsonb','default': "null"}orm"""

    my_date=datetime.date.today()
    # """orm{'name': 'date','type': 'timestamp','default': "null"}orm"""
    def __str__(self):
       return f'id-{self.id}, array-{self.array}, dict-{self.dict}, my_date-{self.my_date}, inner-{self.inner}'


b=MapBuilder(TestJson,'json')
b.AppendField(name_field='id',name_column='id',type_column='SERIAL',default='PRIMARY KEY',pk=True,mode=True)
b.AppendField(name_field='array',name_column='array',type_column='integer[]',default='null')
b.AppendField(name_field='dict',name_column='dict',type_column='jsonb',default='null')
b.AppendField(name_field='my_date',name_column='my_date',type_column='timestamp')
b.AppendField(name_field='inner',name_column='inner',type_column='jsonb',default='null')
b.checkHost()

OrmConnectionPool.init(type_pool=0,minconn=1,maxconn=10,password='postgres', host='localhost', port=5432, user='postgres1', database='test',)
with OrmConnectionPool.getContext() as ctx:
    with OrmConnectionPool.getConnection() as connection:
        with connection.getSession() as session:
            with session.beginTransaction() as tx:
              session.dropTable(TestJson,True)
              session.createTable(TestJson,True)
              session.insert(TestJson())
              for r in session.select(TestJson):
                  print(r)
"""
ORM SESSION: insert:('INSERT INTO "json" ("array", "dict", "inner", "date") VALUES ((%s), (%s), (%s), (%s)) RETURNING "id" ;', [[1, 2, 3, 4], '{"name": "name", "age": 34}', '{"name": "sd", "age": 22}', datetime.date(2024, 12, 1)]) 
ORM SESSION: select:('SELECT "id", "array", "dict", "inner", "date" FROM "json" ;', None) 
id-1, array-[1, 2, 3, 4], dict-{'age': 34, 'name': 'name'}, my_date-2024-12-01 00:00:00, inner-{'age': 22, 'name': 'sd'}
"""