from pgorm import get_host_base, HostItem


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
