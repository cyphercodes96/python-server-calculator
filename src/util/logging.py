import logging
from itertools import chain

log = logging.getLogger('rotating_log')

def trace(level='info'):
    def decorator(fn):
        def wrapper(*v, **k):
            name = fn.__name__
            logfunc = getattr(log, level)
            logfunc("%s(%s)" % (name, ", ".join(map(repr, chain(v, k.values())))))
            return fn(*v, **k)
        return wrapper
    return decorator
