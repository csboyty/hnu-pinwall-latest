# coding: utf-8


from werkzeug.utils import cached_property
from flask.ext.cache import Cache


class CacheableMixin(object):
    __cache_properties__ = None

    def to_cache_dict(self):
        properties = self.__cache_properties__
        rv = dict()
        for key in self.__cache_properties__:
            value = getattr(self, key)
            if isinstance(value, CacheableMixin):
                value = value.to_cache_dict()
            elif isinstance(value, list):
                value = [e.to_cache_dict() if isinstance(e, CacheableMixin) else e for e in value]
            
            rv[key] = value

        return rv


class CacheRegistry(object):
    def __init__(self, app=None, **kwargs):
        self._registry = {}
        if app is not None:
            self.app = app

    def init_app(self, app, **kwargs):
        app.cache_registry = self

    def register(self, name, get_method):
        self._registry.setdefault(name, get_method)

    def lookup(self, name):
        return self._registry[name]

