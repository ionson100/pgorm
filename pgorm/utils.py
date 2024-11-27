import ast
import inspect
import textwrap
import re
from itertools import pairwise
import logging


class StringBuilder:
    _file_str =''

    def __init__(self,string:str=''):
        self._file_str = string

    def Append(self, string:str):
        self._file_str+=string

    def __str__(self):
        return self._file_str;
    def ToString(self):
        return self._file_str


def get_str_doc(s:str|None) ->str|None:
    """
    Ищет в описании prprty строку с границами orm{}orm (orm{(.*?)\}orm)
    :param s: строка описание property
    :return: найденая строка или None
    """
    if s is None:
        return None
    pattern = r'orm{(.*?)\}orm'

    match = re.search(pattern, s.replace('\t','').replace('\r','').replace('\n','').strip())
    if match:
        return  '{'+match.group(1)+'}'
    else:
        return None

def get_attr_docs(cls: type) -> dict[str, str]:
    cls_node = ast.parse(textwrap.dedent(inspect.getsource(cls))).body[0]
    if not isinstance(cls_node, ast.ClassDef):
        raise TypeError("Given object was not a class.")
    out = {}
    for a, b in pairwise(cls_node.body):
        if (
            not isinstance(a, ast.Assign | ast.AnnAssign)
            or not isinstance(b, ast.Expr)
            or not isinstance(b.value, ast.Constant)
            or not isinstance(b.value.value, str)
        ):
            continue
        doc = inspect.cleandoc(b.value.value)
        if isinstance(a, ast.Assign):
            targets = a.targets
        else:
            targets = [a.target]
        for target in targets:
            if not isinstance(target, ast.Name):
                continue
            st=get_str_doc(doc)
            if st is None:
                continue
            logging.debug(f'build attribute- {target.id}:{st}')
            out[target.id] = st
    return out
def get_attribute_all(cls:type)-> dict[str, str]:
    out={}
    res=get_attr_docs(cls)
    for k in res:
        out[k]=res[k]
    t=cls.__base__
    if t==object:
        return out
    else:
       res= get_attr_docs(t)
    for k in res:
        out[k]=res[k]

    return out

def get_attribute_class(cls:type)->str|None:
    """
     Ищет в описании класс, строку с границами orm{}orm (orm{(.*?)\}orm)
    :param s: строка описание класса
    :return: найденная строка или None
    :param cls:
    :return:
    """
    s=cls.__doc__
    s=get_str_doc(s)
    if s is None:
        raise TypeError(f"Тип: {cls} не имеет описания как объект для работы с орм")
    return s