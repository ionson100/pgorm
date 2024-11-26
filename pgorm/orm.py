from __future__ import annotations

from typing import Any, Sequence, Mapping
import logging
import psycopg2

# from .biulderInsert import get_sql_insert
# from .buildUpdate import get_sql_update
from .builderSelect import get_sql_select
# from .builderTable import _create_table
from .hostitem import get_host_base, HostItem
from .session import Session


class Transaction:
    connection: psycopg2.extensions.connection | None = None

    def __init__(self, con: psycopg2.extensions.connection):
        self.connection = con

    def get_status_transaction(self) -> int:
        if self.connection is None:
            raise Exception("Транcакция уже использована")
        else:
            return self.connection.info.transaction_status

    def commit(self):
        if self.connection is None:
            raise Exception("Транcакция уже использована")
        else:
            self.connection.commit()
            self.connection.autocommit = True
            self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_DEFAULT)
            self.connection = None

    def rollback(self):
        if self.connection is None:
            raise Exception("Транcакция уже использована")
        else:
            self.connection.rollback()
            self.connection.autocommit = True
            self.connection.set_isolation_level(level=psycopg2.extensions.ISOLATION_LEVEL_DEFAULT)
            self.connection = None


class _Host:
    connect: psycopg2.extensions.connection = None


_self_host = _Host()
print('init orm')


def ormInitConnect(*, dbname: str, user: str = 'postgres', password: str = 'postgres', host: str = 'localhost',
                   port: int = 5432) -> psycopg2.extensions.connection:
    if _self_host.connect is None:
        _self_host.connect = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        _self_host.connect.autocommit = True

    return _self_host.connect


def ormGetConnect():
    if _self_host.connect is None:
        raise Exception('соединение не создано при старте App!')
    else:

        return _self_host.connect

def getSession():
    return Session(_self_host.connect.cursor())

# def orm_exist_table(cls: type) -> bool:
#     cursor = _self_host.connect.cursor()
#     try:
#         ta = orm_get_attribute(cls).table_name
#         sql = f"""SELECT EXISTS  (
#             SELECT FROM
#                 pg_tables
#             WHERE
#                 schemaname = 'public' AND
#                 tablename  = '{ta}'
#             );"""
#         print(sql)
#
#         cursor.execute(sql)
#
#         for record in cursor:
#             [d] = record
#             return d
#     except Exception as e:
#         print("orm", e)
#         return False
#     finally:
#         cursor.close()


def orm_begin_transaction(level: int | None = None) -> Transaction:
    t = Transaction(_self_host.connect)
    t.connection.autocommit = False
    if level is not None:
        t.connection.set_isolation_level(level)
    return t


def ormGetAttribute(cls: type) ->HostItem:
    return get_host_base().get_hist_type(cls)


# def orm_create_table(cls: type):
#     sql = _create_table(orm_get_attribute(cls))
#     cursor = _self_host.connect.cursor()
#     try:
#         print(sql)
#         cursor.execute(sql)
#         return 1
#     except Exception as e:
#         print("orm", e)
#         return 0
#     finally:
#         cursor.close()


# def orm_truncate_table(cls: type):
#     sql = f'TRUNCATE TABLE "{orm_get_attribute(cls).table_name}"'
#     cursor = _self_host.connect.cursor()
#     try:
#         print(sql)
#         cursor.execute(sql)
#         return 1
#     except Exception as e:
#         print("orm", e)
#         return 0
#     finally:
#         cursor.close()


# def orm_drop_table(cls: type):
#     sql = f'DROP TABLE "{orm_get_attribute(cls).table_name}"'
#     cursor = _self_host.connect.cursor()
#     try:
#         print(sql)
#         cursor.execute(sql)
#         return 1
#     except Exception as e:
#         print("orm", e)
#         return 0
#     finally:
#         cursor.close()


# def orm_insert(ob: any):
#     host: HostItem = orm_get_attribute(type(ob))
#     sql: tuple[Any | None, None] = get_sql_insert(ob, host)
#     print(sql)
#     cursor = _self_host.connect.cursor()
#     try:
#         cursor.execute(sql[0], sql[1])
#         for record in cursor:
#             [d] = record
#             for key, value in host.columns.items():
#                 if value.isPk is True:
#                     setattr(ob, value.name_property, d)
#                     print(d)
#         return 1
#     except Exception as e:
#         print("orm", e)
#         return 0
#     finally:
#         cursor.close()


# def orm_update(ob: any):
#     host: HostItem = orm_get_attribute(type(ob))
#     sql: tuple[Any | None, None] = get_sql_update(ob, host)
#     print(sql)
#     cursor = _self_host.connect.cursor()
#     try:
#         cursor.execute(sql[0], sql[1])
#         return 1
#     except Exception as e:
#         print("orm", e)
#         return 0
#     finally:
#         cursor.close()


# def orm_select(cls: type, where: str = None, *params):
#     host: HostItem = orm_get_attribute(cls)
#     sql = get_sql_select(cls, host)
#     if where is not None:
#         sql += where
#     p = []
#     if params is not None:
#         for param in params:
#             p.append(param)
#     print((sql, p))
#     cursor = _self_host.connect.cursor()
#     try:
#         cursor.execute(sql, p)
#         for record in cursor:
#             index = 0
#             ob = cls()
#             for key, value in host.columns.items():
#                 setattr(ob, key, record[index])
#                 index = index + 1
#             yield ob
#
#     except Exception as e:
#         raise Exception("orm select", e)
#     finally:
#         cursor.close()


# def orm_table_name(cls: type) -> str:
#     c=orm_get_attribute(cls)
#     return c.table_name

# def orm_column_name(cls: type, property_name:str) -> str:
#     for key,value in orm_get_attribute(cls).columns.items():
#         if value.name_property == property_name:
#             return value.name_table
#     raise Exception(f'нозвание колонки асоциированоой для поля {property_name}, в таблице : {cls} отсутствует')


# class Composable:
#     pass


# def orm_execute(sql: str | bytes | Composable,params:Sequence | Mapping[str, Any] | None = None):#Sequence | Mapping[str, Any] | None = None
#     cursor = _self_host.connect.cursor()
#     try:
#
#         cursor.execute(sql, params)
#         logging.debug((sql, params))
#         for record in cursor:
#             yield record
#     except Exception as e:
#         logging.error('orm select',e,exc_info=True)
#     finally:
#         cursor.close()

# def orm_execute_not_query(sql:str,*params):
#     cursor = _self_host.connect.cursor()
#     try:
#         cursor.execute(sql, params)
#         for record in cursor:
#             yield record
#     except Exception as e:
#         raise Exception("orm select", e)
#     finally:
#         cursor.close()
