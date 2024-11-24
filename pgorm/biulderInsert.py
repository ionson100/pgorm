from .hostitem import HostItem, _ColumnData

_dictInsert:dict[type,str]={}




def _inner_builder(h:HostItem,t:type):
    sql=f'INSERT INTO {h.table_name} ('
    for key,value in h.columns.items():
        sql+=f'"{value.name_table}", '
    sql=sql.strip(' ').strip(',')+ ') VALUES ('
    for _, value in h.columns.items():
        sql+='(%s), '
    sql = sql.strip(' ').strip(',') + ') RETURNING '

    for key, value in h.columns.items():
        if value.isPk is True:
            sql+=value.name_table+';'
    print(sql)
    _dictInsert[t]= sql



def _inner_build_param(o:any,h:HostItem):
    d:list[any]=[]
    for key, value in h.columns.items():
        v=getattr(o,key)
        d.append(v)
    return d


def get_sql_insert(o: any ,h:HostItem):


    t=type(o)
    c = _dictInsert.get(t)
    if c is None:
        _inner_builder(h,t)

    return _dictInsert.get(t), _inner_build_param(o, h)
