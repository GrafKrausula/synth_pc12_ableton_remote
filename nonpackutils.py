from pathlib import Path
import traceback
import pathlib


def index_of(seq, item):
    if seq is None:
        return -1

    i = 0
    for n in seq:
        if n == item:
            return i
        i += 1

    return -1

def normalize_relative_value(n):
    return n if n <= 64 else n - 128

def getScriptPath():

    scriptpath = str(pathlib.Path(__file__).parent.absolute())
    return scriptpath


def create_crashlog(message):

    if isinstance(message, str) is False:
        if type(message) is list:
            message = ' '.join(str(e) for e in message)
        else:
            if type(message) is int:
                message = str(message)
            else:
                message = str(type(message))

    path = getScriptPath() + "\CRASH_LOG.txt"
    log_file = open(path, "a")
    log_file.write(message)
    log_file.write("\n\n")
    log_file.close()
    return
