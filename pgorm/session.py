from typing import Sequence, Mapping, Any

import psycopg2
import logging

from pgorm.biulderInsert import get_sql_insert
from pgorm.buildUpdate import get_sql_update
from pgorm.builderSelect import get_sql_select
from pgorm.builderTable import _create_table
from pgorm.hostitem import get_host_base, HostItem
from pgorm.jsonWorker import get_object_from_json
from pgorm.transaction import Transaction
from pgorm.insertBulk import buildInsertBulk


def _get_attribute(cls: type):
    return get_host_base().get_hist_type(cls)


class Session:

    def __init__(self, cursor: psycopg2.extensions.cursor):
        self._cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self._cursor is None:
            logging.error('orm:close session. The session is already closed', exc_info=True)
        else:
            self._cursor.close()
            self._cursor = None

    @staticmethod
    def tableName(cls: type) -> str:
        """Get the name of the table in the database associated with the type"""
        return f'"{_get_attribute(cls).table_name}"'

    @staticmethod
    def columnName(cls: type, property_name: str) -> str:
        """
        Getting the name of a column in a table by the associated field in the type
        :param cls: class
        :param property_name: property name
        :return: str or error
        """
        for key, value in _get_attribute(cls).columns.items():
            if value.name_property == property_name:
                return f'"{value.name_table}"'
        logging.error(
            f'The name of the column associated with the field {property_name}, in the table : {cls} is missing',
            exc_info=True)

    def existTable(self, cls: type) -> bool:
        """Checking for table existence"""
        try:
            ta = _get_attribute(cls).table_name
            sql = f"""SELECT EXISTS  ( SELECT FROM  pg_tables WHERE  schemaname = 'public' AND  tablename  = '{ta}' );"""
            logging.debug(f'orm:exist table.sql:{sql}')
            self._cursor.execute(sql)
            for record in self._cursor:
                [d] = record
                return d
        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def createTable(self, cls: type):
        """Creating a table from a class, the class type must have all attributes to be created"""
        try:
            sql = _create_table(_get_attribute(cls))
            logging.debug(f'orm:create table.sql:{sql}')
            self._cursor.execute(sql)

        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def truncateTable(self, cls: type):
        """
        TRUNCATE quickly removes all rows from a set of tables. It has the same effect as an unqualified DELETE on each table,
        but since it does not actually scan the tables it is faster. Furthermore,
        it reclaims disk space immediately, rather than requiring a subsequent VACUUM operation. This is most useful on large tables.
        """
        try:
            sql = f'TRUNCATE TABLE "{_get_attribute(cls).table_name}";'
            self._cursor.execute(sql)
            logging.debug(f'orm:truncate table.sql:{sql}')
        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def dropTable(self, cls: type):
        """
        DROP TABLE removes tables from the database. Only the table owner, the schema owner, and superuser can drop a table.
        To empty a table of rows without destroying the table, use DELETE or TRUNCATE.
        """
        try:
            sql = f'DROP TABLE "{_get_attribute(cls).table_name}";'
            self._cursor.execute(sql)
            logging.debug(f'orm:drop table.sql:{sql}')
        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def deleteFromTable(self, cls: type, where: str = '',
                        params: Sequence | Mapping[str, Any] | None = None):
        """
        deletes rows that satisfy the WHERE clause from the specified table.
        If the WHERE clause is absent, the effect is to delete all rows in the table. The result is a valid, but empty table.
        By default, DELETE will delete rows in the specified table and all its child tables.
        If you wish to delete only from the specific table mentioned, you must use the deleteFromOnlyTable clause
        :return rows count deleted.
        """
        try:
            sql = f'DELETE FROM "{_get_attribute(cls).table_name}" {where};'
            logging.debug(f'orm:delete table.sql:{sql} {params}')
            self._cursor.execute(sql, params)
            return self._cursor.rowcount

        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def deleteFromOnlyTable(self, cls: type, where: str = '',
                            params: Sequence | Mapping[str, Any] | None = None) ->int:
        """
        deletes rows that satisfy the WHERE clause from the specified table.
        If the WHERE clause is absent, the effect is to delete all rows in the table. The result is a valid, but empty table
        :return rows count deleted.
        """
        try:
            sql = f'DELETE FROM ONLY "{_get_attribute(cls).table_name}" {where};'
            logging.debug(f'orm:delete only table.sql:{sql} {params}')
            self._cursor.execute(sql, params)
            return self._cursor.rowcount

        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def insert(self, ob: any) ->int:
        """
        Inserting an object into a database, the object must have all the attributes that describe it in the database
        :param ob: object to insert
        :return: count of rows affected in the database
        """

        try:
            host: HostItem = _get_attribute(type(ob))
            sql: tuple[any | None, None] = get_sql_insert(ob, host)
            logging.debug(f'orm:insert.sql:{sql}')
            self._cursor.execute(sql[0], sql[1])

            if host.pk_generate_server:
                for record in self._cursor:
                    [d] = record
                    setattr(ob, host.pk_property_name, d)


            return self._cursor.rowcount
        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def update(self, ob: any) ->int:
        """
        Updating an object into a database, the object must have all the attributes that describe it in the database
        :param ob: object to update
        :return: count of rows affected in the database
        """
        try:
            host: HostItem = _get_attribute(type(ob))
            sql: tuple[any | None, None] = get_sql_update(ob, host)
            logging.debug(f'orm:update.sql:{sql}')
            self._cursor.execute(sql[0], sql[1])
            return self._cursor.rowcount

        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def select(self, cls: type, where: str = None,
               params: Sequence | Mapping[str, Any] | None = None) -> list[any]:
        """
        Getting an iterator to a selection from a database
        :param cls: Table type
        :param where: the string in a query that comes after the FROM word
        :param params: array of parameters according to psycopg2 specification
        :return: count of rows affected in the database
        """
        try:
            host: HostItem = _get_attribute(cls)
            sql = get_sql_select(cls, host)
            if where is not None:
                sql += where
            p = []
            if params is not None:
                for param in params:
                    p.append(param)
            logging.debug(f'orm:select.sql:{(sql, p)}')
            self._cursor.execute(sql, p)

            for record in self._cursor:
                index = 0
                ob = cls()
                for key, value in host.columns.items():
                    if value.type.strip()== 'jsonb':
                        v=get_object_from_json(record[index])
                        setattr(ob, key, v)
                    else:
                        setattr(ob, key, record[index])
                    index = index + 1
                yield ob
        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def execute(self, sql: str | bytes,
                params: Sequence | Mapping[str, Any] | None = None):  # Sequence | Mapping[str, Any] | None = None
        """
        Getting an iterator for an arbitrary query string
        :param sql: query string
        :param params: array of parameters according to psycopg2 specification
        :return: count of rows affected in the database
        """

        try:
            self._cursor.execute(sql, params)
            logging.debug(f'orm:execute.sql:{(sql, params)}')
            for record in self._cursor:
                yield record
        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def executeNotQuery(self, sql: str | bytes,
                        params: Sequence | Mapping[
                            str, Any] | None = None) ->int:  # Sequence | Mapping[str, Any] | None = None
        """
        Execute a query without returning a result
        :param sql: query string
        :param params: array of parameters according to psycopg2 specification
        :return: count of rows affected in the database
        """
        try:
            logging.debug(f'orm:executeNotQuery.sql:{(sql, params)}')
            self._cursor.execute(sql, params)
            return self._cursor.rowcount
        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

    def beginTransaction(self, level: int | None = None) -> Transaction:
        """
        Getting a transaction to execute a request
        :param level: insulation level
        :return: Transaction
        """

        t = Transaction(self._cursor.connection,level)


        return t

    def insertBulk(self, ob: [any]) ->int:
        """
        Batch insert an array of objects into a database.
        All objects must be of the same type.
        The type must have description attributes for the database
        :param ob: Array of objects
        :return: count of rows affected in the database
        """
        try:
            if len(ob)==0:
                return 0
            host: HostItem = _get_attribute(type(ob[0]))
            sql = buildInsertBulk(host, *ob)
            logging.debug(f'orm:insertBulk.sql:{sql}')
            self._cursor.execute(sql[0], sql[1])
            index = 0
            if host.pk_generate_server:
                for record in self._cursor:
                    setattr(ob[index], host.pk_property_name, record)
                    index = index + 1


            return self._cursor.rowcount
        except Exception as exc:
            logging.error("%s: %s" % (exc.__class__.__name__, exc))
            raise
    def cancel(self):
        self._cursor.connection.cancel()

