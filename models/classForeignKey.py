import uuid


class ForeignKey:
    """orm{'name':'ForeignKey'}orm"""
    id: str
    """orm{'name':'_Id_key','type':'uuid ',  'default':'PRIMARY KEY','pk':True, }orm"""
    name: str;
    """orm{'name':'Name_key','type':'TEXT',  'default':'DEFAULT NULL'}orm"""
    id_test: str;
    """orm{'name':'id_test','type':'uuid',  'default':'DEFAULT NULL'}orm"""

    def __init__(self):
        self.name = 'asas'
        self.id = str(uuid.uuid4())