import uuid

from models.classForeignKey import ForeignKey
from models.classJsonTest import JsonTest
from pgorm.decoratorForeignKey import  getRelatives


class Test221:
    """orm{'name':'test221'}orm"""
    id: str
    """orm{'name':'_Id','type':'uuid ',  'default':'PRIMARY KEY','pk':True, }orm"""
    name: str
    """orm{'name':'Name','type':'TEXT',  'default':'DEFAULT NULL'}orm"""

    jsonB: any
    """orm{'name':'json','type':'jsonb',  'default':' default null'}orm"""

    def __init__(self, name: str | None = None):
        self.id = str(uuid.uuid4())
        self.name = "ewe"
        if name is not None:
            self.name = name
        self.jsonB = JsonTest()

    def __str__(self):
        return str((self.id, self.name, self.jsonB))
    @getRelatives(ForeignKey, 'id_test')
    def getForeignObject(self):
       pass