import json
import uuid


class Test22:
    """orm{'name':'test22'}orm"""
    id: int = 0
    """orm{'name':'_id','type':'SERIAL ',  'default':'PRIMARY KEY','pk':True, 'mode':True}orm"""
    name: str
    """orm{'name':'name','type':'TEXT',  'default':'DEFAULT NULL'}orm"""

    def __init__(self, name: str | None = None):
        self.name = "ewe"
        if name is not None:
            self.name = name

    def __str__(self):
        return str((self.id, self.name))


