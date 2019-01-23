import datetime
from dateutil import parser, tz


def utcnow():
    dt = datetime.datetime.utcnow()
    dt = dt.replace(tzinfo=tz.gettz('UTC'))
    return dt


def parse(dt):
    try:
        dt = parser.parse(dt)
    except Exception as e:
        raise ValueError("Unknown date format: '%s'" % str(dt))
    if not dt.tzinfo:
        raise ValueError("Time '%s' doesn't contain timezone information" % str(dt))
    return dt

