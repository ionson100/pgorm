import os




class _print_settings:
    _print: bool

    def __init__(self, use_print=False):
        self._print = use_print

    @property
    def print(self):
        return self._print


_host_print_settings: _print_settings = _print_settings(False)


def set_print(use_print: bool):
    _host_print_settings._print = use_print


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'


os.system("")


def PrintExecutes(*msg: str):
    if _host_print_settings.print is False:
        return
    s = 'ORM SESSION: '
    for i in msg:
        s += str(i).strip() + ' '

    print(bcolors.OKGREEN + f'{s}' + '\x1b[0m')


def PrintAttribite(*msg):
    if _host_print_settings._print is False:
        return
    s = 'ORM BUILD ATTRIBUTE: '
    for i in msg:
        s += str(i).strip() + ' '

    print(bcolors.OKGREEN + f'{s}' + '\x1b[0m')


def PrintFree(*msg):
    if _host_print_settings._print == False:
        return
    s = ''
    for i in msg:
        s += str(i).strip() + ' '

    print(bcolors.OKGREEN + f'{s}' + '\x1b[0m')
