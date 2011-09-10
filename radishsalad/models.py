#! /usr/bin/env python

from itertools import izip
from .connection import get_redis
from . import datatypes
from .errors import RadishSaladError
from .utils import StringMixin, ichain

# Redis datatypes

class DataType(datatypes.RedisDataType):

    def __get__(self, instance, owner):
        new_inst = type(self)(*getattr(self, 'args', []),
                              **getattr(self, 'kwargs', {}))
        new_inst._key = self._key
        new_inst.instance = instance or owner
        new_inst._value = getattr(new_inst.instance, 'cache', {}).get(self._key)
        return new_inst

    def get_key(self, instance=None, custom_id=None):
        inst = instance or self.instance
        oid = getattr(inst, 'id', custom_id)
        if oid is None:
            raise RadishSaladError(
                    'You need call this method with instance or id')
        return '%s:%s:%s' % (inst.prefix, oid, self._key)

    def gen_keys(self, seq):
        return [self.get_key(custom_id=custom_id) for custom_id in seq]


class String(DataType, StringMixin, datatypes.String):

    def __set__(self, instance, value):
        self._value = value
        get_redis().set(self.get_key(instance), value)


class Hash(DataType, datatypes.Hash):
    pass


class List(DataType, datatypes.List):
    pass


class Set(DataType, datatypes.Set):
    pass


class AutoIncrementId(object):

    def __get__(self, instance, owner):
        return  datatypes.Counter('counter:' + owner.prefix)


class Pointer(String):
    def __init__(self, foreign_class):
        self.foreign_class = foreign_class
        self.args = [foreign_class]

    def __get__(self, instance, owner):
        return self.foreign_class(
                str(super(Pointer, self).__get__(instance, owner)))


# Base for models

class ModelMetaclass(type):
    prefixes = []

    def __new__(cls, name, bases, attrs):
        strings = []
        for key, attr in attrs.iteritems():
            if isinstance(attr, DataType):
                attr.set_key(key)
            # Keep strings for MGET
            if isinstance(attr, String):
                strings.append(key)
        if not 'prefix' in attrs:
            attrs['prefix'] = name.lower()
        if attrs['prefix'] in ModelMetaclass.prefixes:
            raise Exception('Duplication of prefixies')
        # Developer can put his own prefetching list
        if 'strings' not in attrs:
            attrs['strings'] = strings
        ModelMetaclass.prefixes.append(attrs['prefix'])
        return type.__new__(cls, name,bases, attrs)


class Model(object):
    __metaclass__ = ModelMetaclass

    id_generator = AutoIncrementId()

    def __init__(self, oid=None, new=False, cache=None):
        if new and oid is None:
            self.id = str(self.id_generator.next())
        elif oid is not None:
            self.id = oid
        else:
            raise ValueError('Do you want create object or what?')
        self.cache = dict(zip(self.strings, (v or '' for v in cache))) if cache else {}

    @classmethod
    def get_strings(cls):
        return [getattr(cls, s) for s in cls.strings]

    @classmethod
    def from_seq(cls, seq):
        seq = list(seq)
        redis = get_redis()
        strs = cls.get_strings()
        prefetch_keys = list(ichain(izip(*[s.gen_keys(seq) for s in strs])))
        data = redis.mget(prefetch_keys)
        nstr = len(cls.strings)
        return [cls(id, cache=[data.pop(0) for i in xrange(nstr)]) for id in seq]
