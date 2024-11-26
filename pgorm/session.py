from typing import Sequence, Mapping, Any

import psycopg2
import logging

from pgorm.biulderInsert import get_sql_insert
from pgorm.buildUpdate import get_sql_update
from pgorm.builderSelect import get_sql_select
from pgorm.builderTable import _create_table
from pgorm.hostitem import get_host_base, HostItem


def _get_attribute(cls: type):
    return get_host_base().get_hist_type(cls)



class Session:


    def __init__(self, cursor: psycopg2.extensions.cursor):
        self._cursor = cursor

    def close(self):
        if self._cursor is None:
            logging.error('orm:close session. The session is already closed', exc_info=True)
        else:
            self._cursor.close()
            self._cursor = None

    def tableName(self,cls:type) ->str:
        return _get_attribute(cls).table_name

    def columnName(self,cls: type, property_name:str) ->str:
        for key, value in _get_attribute(cls).columns.items():
            if value.name_property == property_name:
                return value.name_table
        logging.error(f'нозвание колонки асоциированоой для поля {property_name}, в таблице : {cls} отсутствует', exc_info=True)

    def existTable(self, cls: type) -> bool:
        try:
            ta = _get_attribute(cls).table_name
            sql = f"""SELECT EXISTS  (
                        SELECT FROM 
                            pg_tables
                        WHERE 
                            schemaname = 'public' AND 
                            tablename  = '{ta}'
                        );"""
            logging.debug(f'orm:exist table.sql:{sql}')
            self._cursor.execute(sql)
            for record in self._cursor:
                [d] = record
                return d
        except Exception as e:
            logging.error('orm:exist table.', e, exc_info=True)

    def createTable(self, cls: type):
        try:
            sql = _create_table(_get_attribute(cls))
            self._cursor.execute(sql)
            logging.debug(f'orm:create table.sql:{sql}')
        except Exception as e:
            logging.error('orm:create table.', e, exc_info=True)

    def truncateTable(self, cls: type):
        try:
            sql = f'TRUNCATE TABLE {_get_attribute(cls).table_name}'
            self._cursor.execute(sql)
            logging.debug(f'orm:trunczte table.sql:{sql}')
        except Exception as e:
            logging.error('orm:truncate table.', e, exc_info=True)

    def dropTable(self, cls: type):
        try:
            sql = f'DROP TABLE {_get_attribute(cls).table_name}'
            self._cursor.execute(sql)
            logging.debug(f'orm:truncate table.sql:{sql}')
        except Exception as e:
            logging.error('orm:truncate table.', e, exc_info=True)

    def insert(self, ob: any):
        try:
            host: HostItem = _get_attribute(type(ob))
            sql: tuple[any | None, None] = get_sql_insert(ob, host)
            self._cursor.execute(sql[0], sql[1])
            logging.debug(f'orm:insert.sql:{sql}')
            for record in self._cursor:
                [d] = record
                for key, value in host.columns.items():
                    if value.isPk is True:
                        setattr(ob, value.name_property, d)
                    return 1
        except Exception as e:
            logging.error('orm:insert.', e, exc_info=True)

    def update(self,ob:any):
        try:
            host: HostItem = _get_attribute(type(ob))
            sql: tuple[any | None, None] = get_sql_update(ob, host)
            self._cursor.execute(sql[0], sql[1])
            logging.debug(f'orm:update.sql:{sql}')
        except Exception as e:
            logging.error('orm:update.', e, exc_info=True)

    def select(self,cls: type, where: str = None, *params):
        try:
            host: HostItem = _get_attribute(cls)
            sql = get_sql_select(cls, host)
            if where is not None:
                sql += where
            p = []
            if params is not None:
                for param in params:
                    p.append(param)
            self._cursor.execute(sql, p)
            #logging.debug(f'orm:select.sql:{(sql,p)}')
            for record in self._cursor:
                index = 0
                ob = cls()
                for key, value in host.columns.items():
                    setattr(ob, key, record[index])
                    index = index + 1
                yield ob
        except Exception as e:
            logging.error('orm:select.', e, exc_info=True)

    def execute(self,sql: str | bytes,
                    params: Sequence | Mapping[str, Any] | None = None):  # Sequence | Mapping[str, Any] | None = None

        try:
            self._cursor.execute(sql, params)
            logging.debug(f'orm:execute.sql:'(sql, params))
            for record in self._cursor:
                yield record
        except Exception as e:
            logging.error('orm execute', e, exc_info=True)

    def executeNotQuery(self, sql: str | bytes,
                params: Sequence | Mapping[str, Any] | None = None):  # Sequence | Mapping[str, Any] | None = None

        try:
            self._cursor.execute(sql, params)
            logging.debug(f'orm:executeNotQuery.sql:'(sql, params))

        except Exception as e:
            logging.error('orm executeNotQuery', e, exc_info=True)




