from .hostitem import HostItem
def _portion(h:HostItem, ob:any, p:list[any]):
    s='('
    for key, valur in h.columns.items():
        s=s+"%s, "
        p.append(getattr(ob,key))
    s=s.strip(' ').strip(',')+'), '
    return s

def buildInsertBulk(h:HostItem,*ob)->(str,list[any]):
    params:list[any]=[]
    sql=f'INSERT INTO {h.table_name} ('
    for key,value in h.columns.items():
        sql=sql+f'"{value.name_table}", '
    sql=sql.rstrip(' ').strip(',')+') VALUES '
    for o in ob:
        sql= sql +_portion(h, o, params)
    sql=sql.strip(' ').strip(',')+ ' RETURNING '

    for key, value in h.columns.items():
        if value.isPk is True:
            sql += f'"{value.name_table}" ;'
    return (sql,params)



