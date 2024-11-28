from multiprocessing.managers import Value
from typing import Sequence, Mapping, Any

from psycopg.generators import execute

from pgorm.hostitem import get_host_base, HostItem
from pgorm.builderSelect import get_sql_select
from pgorm.orm import OrmConnection
import logging


def getRelatives(cls: type,fk:str, add_where: str = None,
               params: Sequence | Mapping[str, Any] | None = None):
    def decorator(func):
        def wrapper(self):
            try:
                logging.debug(f"Decorator arguments: {cls}, {fk}, {add_where}, {params}, {type(self)}")
                host: HostItem = get_host_base().get_hist_type(type(self))
                name_key = host.pk_property_name
                host_core = get_host_base().get_hist_type(cls)
                value_key = getattr(self, name_key)
                r = hasattr(self, value_key)
                if hasattr(self, value_key):
                    return getattr(self, value_key)
                else:
                    p = []
                    sql = get_sql_select(cls, host_core) + f"WHERE {fk} = %s "
                    p.append(value_key)
                    if add_where is not None:
                        sql += add_where
                    sql += ';'

                    if params is not None:
                        for param in params:
                            p.append(param)
                    logging.debug(f'orm:decorator.sql:{(sql, p)}')
                    session = OrmConnection.getSession()

                    result_list: list[cls] = []
                    for r in session.execute(sql, tuple(p)):
                        result_list.append(r)
                    setattr(self, value_key, result_list)

                    return getattr(self, value_key)
            except Exception as exc:
                logging.error("%s: %s" % (exc.__class__.__name__, exc))
                raise
        return wrapper
    return decorator


