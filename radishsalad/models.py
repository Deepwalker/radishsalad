#! /user/bin/env python

from .connection import get_redis
from . import datatypes

# Redis datatypes

class DataType(datatypes.RedisDataType):

    def __get__(self, instance, owner):
        new_inst = type(self)(*getattr(self, 'args', []),
                              **getattr(self, 'kwargs', {}))
        new_inst._key = self._key
        new_inst.instance = instance
        return new_inst

    def get_key(self, instance=None):
        inst = instance or self.instance
        return '%s:%s:%s' % (inst.prefix, inst.id, self._key)


class String(DataType, datatypes.String):

    def __set__(self, instance, value):
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
        for key, attr in attrs.iteritems():
            if isinstance(attr, DataType):
                attr.set_key(key)
        if not 'prefix' in attrs:
            attrs['prefix'] = name.lower()
        if attrs['prefix'] in ModelMetaclass.prefixes:
            raise Exception('Duplication of prefixies')
        ModelMetaclass.prefixes.append(attrs['prefix'])
        return type.__new__(cls, name,bases, attrs)


class Model(object):
    __metaclass__ = ModelMetaclass

    id_generator = AutoIncrementId()

    def __init__(self, oid=None, new=False):
        if new and oid is None:
            self.id = str(self.id_generator.next())
        elif oid is not None:
            self.id = oid
        else:
            raise ValueError('Do you want create object or what?')

    @classmethod
    def from_seq(cls, seq):
        return [cls(id) for id in seq]
