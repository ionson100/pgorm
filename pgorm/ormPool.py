import logging
import psycopg2
import psycopg2.pool
from .hostitem import get_host_base, HostItem
from .session import Session
import enum



class _HostPool:
    pool: psycopg2.pool = None


_self_host_pool = _HostPool()

class OrmConnectionPool:
    @staticmethod
    def init(*,type_pool:int, minconn:int, maxconn:int, user:str, password:str, host:str, port:int,  database:str):
        """
                 user="",
                 password="1",
                 host="",
                 port="",
                 database=""
                :param type_pool 1-SimpleConnectionPool other value=ThreadedConnectionPool, default:1
                :param minconn: min connection init start
                :param maxconn: max connection
                :param args: array settings connections
                :param kwargs: dictionary settings connections
                """
        if type_pool == 0:
            _self_host_pool.pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn,
                                 user=user, password=password, host=host, port=port,  database=database)
        else:
            _self_host_pool.pool = psycopg2.pool.ThreadedConnectionPool(minconn, maxconn,
                                 user=user, password=password, host=host, port=port,  database=database)

    def __int__(self):
        pass


    @staticmethod
    def GetConnection():
        return ConnectionPool(_self_host_pool.pool)
    @staticmethod
    def ClosePool():
        _self_host_pool.pool.closeall
        _self_host_pool.pool = None



class ConnectionPool:
    _connection:psycopg2.extensions.connection
    def __init__(self,pool:psycopg2.pool):
        self._connection=pool.getconn()
    def __enter__(self):
        return self;
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeConnection()

    def closeConnection(self):
        _self_host_pool.pool.putconn(self._connection)
    def getConnection(self):
        """Getting a connection for independent work"""
        return self._connection
    def getSession(self):
        return Session(self._connection.cursor())






