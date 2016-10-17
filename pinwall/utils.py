# coding:utf-8

"""
    enum see http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/
"""
from dateutil import tz, parser
from itsdangerous import text_type
import datetime
import os
import zipfile
import cchardet


class EnumSymbol(object):
    """Define a fixed symbol tied to a parent class. """

    def __init__(self, cls_, name, value, description):
        self.cls_ = cls_
        self.name = name
        self.value = value
        self.description = description

    def __reduce__(self):
        """Allow unpickling to return the symbol linked to the DeclEnum class."""
        return getattr, (self.cls_, self.name)

    def __iter__(self):
        return iter([self.value, self.description])

    def __repr__(self):
        return "<%s>" % self.name


class EnumMeta(type):
    """Generate new DeclEnum classes."""

    def __init__(cls, classname, bases, dict_):
        cls._reg = reg = cls._reg.copy()
        for k, v in dict_.items():
            if isinstance(v, tuple):
                sym = reg[v[0]] = EnumSymbol(cls, k, *v)
                setattr(cls, k, sym)
        return type.__init__(cls, classname, bases, dict_)

    def __iter__(cls):
        return iter(cls._reg.values())


class DeclEnum(object):
    """Declarative enumeration."""

    __metaclass__ = EnumMeta
    _reg = {}

    @classmethod
    def value_of(cls, value):
        try:
            return cls._reg[value]
        except KeyError:
            raise ValueError("Invalid value for %r: %r" % (cls.__name__, value))

    @classmethod
    def values(cls):
        return cls._reg.keys()


class AttrDict(dict):
    """A dictionary with attribute-style access. It maps attribute access to
    the real dictionary.  """

    def __init__(self, init={}):
        dict.__init__(self, init)

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        return super(AttrDict, self).__setitem__(key, value)

    def __getitem__(self, name):
        try:
            item = super(AttrDict, self).__getitem__(name)
            return AttrDict(item) if type(item) == dict else item
        except KeyError:
            return None

    def __delitem__(self, name):
        return super(AttrDict, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__
    __delattr__ = __delitem__

    def copy(self):
        ch = AttrDict(self)
        return ch


def equal_ignore_none_empty_string(o1, o2):
    r = o1 == o2
    if not r:
        if o1 is None and o2 == "":
            return True
        if o1 == "" and o2 is None:
            return True

    return r


def utc_to_localtime(dt_str):
    local_tz = tz.gettz()
    dt = parser.parse(dt_str).astimezone(local_tz)
    return dt


def format_datetime(dt):
    if dt and isinstance(dt, datetime.datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif dt and isinstance(dt, text_type):
        return dt
    else:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def format_date(dt):
    if dt and isinstance(dt, datetime.datetime):
        return dt.strftime('%Y-%m-%d')
    elif dt and isinstance(dt, text_type):
        return dt
    else:
        None


def parse_datetime(dt_str):
    return datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')


def unzip(filename, basedir):
    zfile = zipfile.ZipFile(filename, "r")
    for name in zfile.namelist():
        if type(name) != unicode:
            encoding = cchardet.detect(name)['encoding']
            if encoding == 'UTF-8':
                unicode_name = name.decode('utf-8')
            elif encoding == 'ASCII':
                unicode_name = name
            else:
                unicode_name = name.decode(encoding,'ignore')
        else:
            unicode_name = name
        try:
            f_name = os.path.join(basedir, unicode_name).encode('utf-8')
            pathname = os.path.dirname(f_name)
            if not os.path.exists(pathname) and pathname != "":
                os.makedirs(pathname)
            data = zfile.read(name)
            if not os.path.exists(f_name):
                fo = open(f_name, "w")
                fo.write(data)
                fo.close
        except Exception as e:
            print e
            continue

    zfile.close()


