#! /user/bin/env python

from .connection import get_redis
from . import datatypes

# Redis datatypes

class DataType(datatypes.RedisDataType):
    def __get__(self, instance, owner):
        new_inst = self.__class__()
        new_inst._key = self._key
        new_inst.instance = instance
        return new_inst

    def get_key(self, instance=None):
        return self._key + str((instance or self.instance).id)


class String(DataType):
    def __get__(self, instance, owner):

        return get_redis().get(self.get_key(instance))

    def __set__(self, instance, value):
        get_redis().set(self.get_key(instance), value)


class Hash(DataType, datatypes.Hash):
    pass


class List(DataType, datatypes.List):
    pass


class Set(DataType, datatypes.Set):
    pass


# Base for models

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        for key, attr in attrs.iteritems():
            if isinstance(attr, DataType):
                attr.set_key(key)
        return type.__new__(cls, name,bases, attrs)


class Model(object):
    __metaclass__ = ModelMetaclass

    def __init__(self, id):
        # TODO new object creation by id generation
        self.id = id
