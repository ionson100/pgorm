import uuid
import logging

from models.classForeignKey import ForeignKey
from models.classJsonTest import JsonTest
from pgorm.decoratorForeignKey import  getRelatives
from pgorm.session import Session

logging.basicConfig(level=logging.DEBUG)
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

    @getRelatives(ForeignKey,Session.columnName(ForeignKey,"id_test"),
                  f'and {Session.columnName(ForeignKey,'name')} = %s',['asas'])
    def getForeignObject(self) ->list[ForeignKey]:
       pass