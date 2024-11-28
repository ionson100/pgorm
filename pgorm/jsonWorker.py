import json
from time import time


def get_json(ob:any) ->str:
    if ob is None:
        return None
    if hasattr(ob, 'toJson'):
         return ob.toJson()
    else:
        j = str(json.dumps(ob),default='toJson')
        return j




def get_object_from_json(o:any):
    if o is None:
        return None
    return o

def safe_serialize(obj , max_depth = 2):

    max_level = max_depth

    def _safe_serialize(obj , current_level = 0):

        nonlocal max_level

        # If it is a list
        if isinstance(obj , list):

            if current_level >= max_level:
                return "[...]"

            result = list()
            for element in obj:
                result.append(_safe_serialize(element , current_level + 1))
            return result

        # If it is a dict
        elif isinstance(obj , dict):

            if current_level >= max_level:
                return "{...}"

            result = dict()
            for key , value in obj.items():
                result[f"{_safe_serialize(key , current_level + 1)}"] = _safe_serialize(value , current_level + 1)
            return result

        # If it is an object of builtin class
        elif hasattr(obj , "__dict__"):
            if hasattr(obj , "__repr__"):
                result = f"{obj.__repr__()}_{int(time())}"
            else:
                try:
                    result = f"{obj.__class__.__name__}_object_{int(time())}"
                except:
                    result = f"object_{int(time())}"
            return result

        # If it is anything else
        else:
            return obj

    return _safe_serialize(obj)
