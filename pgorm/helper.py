import logging

from pgorm import get_host_base, HostItem, get_sql_select
from pgorm.session import _get_attribute


def getAttribute(cls: type) -> HostItem:
    """Get all attributes that describe a type in the database"""
    return get_host_base().get_hist_type(cls)


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


def getSqlForType(cls: type):
    host: HostItem = _get_attribute(cls)
    sql = get_sql_select(cls, host)
    return sql


def tableName(cls: type) -> str:
    """Get the name of the table in the database associated with the type"""
    return f'"{_get_attribute(cls).table_name}"'


def columnName(cls: type, field_name: str) -> str:
    """
    Getting the name of a column in a table by the associated field in the type
    :param cls: class
    :param field_name: property name
    :return: str or error
    """
    for key, value in _get_attribute(cls).columns.items():
        if value.name_property == field_name:
            return f'"{value.name_table}"'
    logging.error(
        f'The name of the column associated with the field {field_name}, in the table : {cls} is missing',
        exc_info=True)
