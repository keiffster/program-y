import os


def get_os_specific_path():
    if os.name == 'posix':
        return '/tmp/'
    elif os.name == 'nt':
        return ''
    else:
        raise Exception("Unknown OS [%s]" % os.name)
