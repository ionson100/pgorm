import json
import uuid
import datetime


class Test:
    """
    Тестовый класс\n
    orm{'name':'test'}orm
    """

    id: uuid
    """
    Эта первичный ключ\n
    orm{
    'name': 'id',
    'type': 'uuid',
    'default': "DEFAULT '00000000-0000-0000-0000-000000000000' ",
    'pk': True
    }orm

    """
    my_list:list[int]
    """orm{'name': 'list', 'type': 'integer[]', 'default': 'null ', 'pk': False}orm"""


    my_date: datetime
    """orm{'name': 'date', 'type': 'timestamp', 'default': 'null ', 'pk': False}orm"""

    name2: str = 'sdsd'
    """
    sasasi isoais i
    """

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.my_date = datetime.datetime.now()
        self.my_list=[1,2,3]


    def __str__(self):
        """
        saaspaos osapospaos
        :return:
        """
        return str((self.id,self.name,self.age,self.my_date,self.my_list))

    name: str
    """orm{'name':'name','type':'TEXT',  'default':'DEFAULT NULL'}orm"""
    age: int=23
    """orm{'name': 'age', 'type': 'integer', 'default': 'DEFAULT 0'}orm"""

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __json__(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)