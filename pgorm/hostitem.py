
from .utils import *


class _DescriptorColumn:
    name:str
    type:str
    default:object
    pk:bool
class _DescriptorTable:
    name:str
    other:str|None

class _ColumnData:
    name_table:str|None=None
    name_property:str|None=None
    type:str|None=None
    isPk:bool=False
    mode_generate_pk_server:bool=False
    default:object|None=None
class HostItem:
    table_name:str|None=None
    table_other:str|None=None
    pk_column_name:str|None=None
    pk_property_name:str|None=None
    pk_generate_server: bool = False # key generation occurs on the server
    columns:dict[str,_ColumnData]={}
class HostAttribute:
    dictHost:dict[str,HostItem]={}

    def add_attribute(self,cls:type):

        json_str= get_attribute_class(cls)
        table=ast.literal_eval(json_str)
        host_item=HostItem()
        host_item.columns={}

        host_item.table_name = None if table.get('name') is None else table.get("name")
        host_item.table_other=None if table.get('other') is None else table.get("other")
        if host_item.table_name is None:
            raise Exception(f'Table name is not defined: {json_str}')
        columns=get_attribute_all(cls)

        for key, value in columns.items():
            column_data=_ColumnData()
            column_data.name_property=key
            col=ast.literal_eval(value)
            column_data.name_table=None if col.get('name') is None else col['name']
            column_data.type=None if col.get('type') is None else col['type']
            column_data.default=None if col.get('default') is None else col['default']
            column_data.isPk=False if col.get('pk') is None else col.get('pk')
            column_data.mode_generate_pk_server = False if col.get('mode') is None else col.get('mode')
            if column_data.isPk:
                host_item.pk_generate_server=column_data.mode_generate_pk_server
                host_item.pk_column_name=column_data.name_table
                host_item.pk_property_name=column_data.name_property
            host_item.columns[key]=column_data
            if column_data.name_table is None:
                raise Exception(f'Table field name is not defined: {value}')

        self.dictHost[str(cls)]=host_item



    def get_hist_type(self,cls:type) ->HostItem:
        res=self.dictHost.get(str(cls))
        if res is None:
            self.add_attribute(cls)
        return self.dictHost.get(str(cls))
hostBase=HostAttribute()
def get_host_base():
    return hostBase









