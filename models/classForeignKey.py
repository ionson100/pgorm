import uuid
from dataclasses import dataclass

from pgorm import getTemplateTableAttributesDoc

#print(getTemplateTableAttributesDoc(name="_id",type_column="SERIAL",default='PRIMARY KEY',pk=True,mode=True))

@dataclass
class ForeignKey:
    "orm{'name':'ForeignKey'}orm"
    id: str
    """orm{'name': '_id', 'type': 'SERIAL', 'default': 'PRIMARY KEY', 'pk': True, 'mode': True}orm"""
    name: str
    """orm{'name':'Name_key','type':'TEXT',  'default':'DEFAULT NULL'}orm"""
    id_test: str
    """orm{'name':'id_test','type':'uuid',  'default':'DEFAULT NULL'}orm"""

    def __init__(self):
        self.name = 'asas'
        self.id = str(uuid.uuid4())

    def __str__(self):
        return f'class: ForeignKey name={self.name} id={self.id}'

# ForeignKey.__doc__=
# ForeignKey.id__doc__=getTemplateTableAttributesDoc(name="_id",type_column="SERIAL",default='PRIMARY KEY',pk=True,mode=True)
