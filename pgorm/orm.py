from __future__ import annotations

from typing import Any, Sequence, Mapping
import logging
import psycopg2
from .builderSelect import get_sql_select
from .hostitem import get_host_base, HostItem
from .session import Session


class _Host:
    connect: psycopg2.extensions.connection = None


_self_host = _Host()


class OrmConnection:
    """Basic type for working with orm, initializing a connection, getting a session"""

    def __init__(self, *, dbname: str, user: str = 'postgres', password: str = 'postgres', host: str = 'localhost',
                 port: int = 5432):
        """Initialization of the ORM is usually required at the beginning of the program."""
        if _self_host.connect is None:
            _self_host.connect = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
            _self_host.connect.autocommit = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        OrmConnection.connectionClose()

    @staticmethod
    def getConnection():
        """Getting a connection for independent work"""
        if _self_host.connect is None:
            logging.error('orm getConnection: connection not created when starting App!', exc_info=True)
        else:
            return _self_host.connect

    @staticmethod
    def getSession():
        """Get a lightweight session to work with the database, close it when finished"""
        if _self_host.connect is None:
            logging.error('orm getConnection: connection not created when starting App!', exc_info=True)
        else:
            return Session(_self_host.connect.cursor())


    @staticmethod
    def connectionClose():
        """Closing the connection"""
        _self_host.connect.close()
        _self_host.connect = None

    @staticmethod
    def getAttribute(cls: type) -> HostItem:
        """Get all attributes that describe a type in the database"""
        return get_host_base().get_hist_type(cls)

    @staticmethod
    def getTemplateTableAttributesDoc(*, name: str, default: str = 'null', typeColumn: str = 'TEXT',
                                      pk: bool = False):
        """Getting a property description string for a database"""
        dec: dict[str, any] = {'name': name, 'type': typeColumn, 'default': default, 'pk': pk}
        return 'orm' + str(dec) + 'orm'
