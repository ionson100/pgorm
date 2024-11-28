from __future__ import annotations

import logging
import psycopg2
from .hostitem import get_host_base, HostItem
from .session import Session


class _Host:
    connect: psycopg2.extensions.connection = None


_self_host = _Host()


class OrmConnection:
    """Basic type for working with orm, initializing a connection, getting a session"""

    def __init__(self, dsn=None, connection_factory=None, cursor_factory=None, **kwargs):
        """
        Create a new database connection.

    The connection parameters can be specified as a string:

        conn = psycopg2.connect("dbname=test user=postgres password=secret")

    or using a set of keyword arguments:

        conn = psycopg2.connect(database="test", user="postgres", password="secret")

    Or as a mix of both. The basic connection parameters are:

    - *dbname*: the database name
    - *database*: the database name (only as keyword argument)
    - *user*: user name used to authenticate
    - *password*: password used to authenticate
    - *host*: database host address (defaults to UNIX socket if not provided)
    - *port*: connection port number (defaults to 5432 if not provided)

    Using the *connection_factory* parameter a different class or connections
    factory can be specified. It should be a callable object taking a dsn
    argument.

    Using the *cursor_factory* parameter, a new default cursor factory will be
    used by cursor().

    Using *async*=True an asynchronous connection will be created. *async_* is
    a valid alias (for Python versions where ``async`` is a keyword).

    Any other keyword parameter will be passed to the underlying client
    library: the list of supported parameters depends on the library version.
        """
        if _self_host.connect is None:
            _self_host.connect = psycopg2.connect(dsn, connection_factory, cursor_factory, **kwargs)
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
        """ close() -- Close the connection. """
        _self_host.connect.close()
        _self_host.connect = None

    @staticmethod
    def getAttribute(cls: type) -> HostItem:
        """Get all attributes that describe a type in the database"""
        return get_host_base().get_hist_type(cls)

    @staticmethod
    def getTemplateTableAttributesDoc(*, name: str, default: str = 'null', type_column: str = 'TEXT',
                                      pk: bool = False, mode: bool = False):
        """
        Getting a property description string for a database
        :param mode: who generates the primary key value False: user generated, True: server generated
        :param name: column name in table
        :param default: default value
        :param type_column: column type
        :param pk: is it a primary key
        :return: a string that can be inserted into the description of a type property
        """
        dec: dict[str, any] = {'name': name, 'type': type_column, 'default': default, 'pk': pk, 'mode': mode}
        return 'orm' + str(dec) + 'orm'
