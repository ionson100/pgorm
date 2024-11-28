



def getRelatives(cls:type, fk:str):
    def decorator(func):
        def wrapper(self):
            print(f"Decorator arguments: {cls}, {fk}, {type(self)}")
            return "989898"
        return wrapper
    return decorator


