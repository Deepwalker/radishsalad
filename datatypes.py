#! /user/bin/env python

from UserDict import DictMixin
from redis.exceptions import ResponseError
from .connection import get_redis


class RedisDataType(object):

    def __init__(self, key=None):
        if key:
            self.set_key(key)

    def get_key(self):
        return self._key

    def set_key(self, key):
        self._key = key

    def r_call(self, redis_command, *args):
        return getattr(get_redis(), redis_command)(self.get_key(), *args)

    def clear(self):
        self.r_call('delete')


class Counter(RedisDataType):
    def next(self):
        return self.r_call('incr')


class String(RedisDataType):
    def __str__(self):
        return self.r_call('get') or ''

    def set(self, value):
        return self.r_call('set', value)


class Hash(RedisDataType, DictMixin):

    def __getitem__(self, key):
        return self.r_call('hget', key)

    def __setitem__(self, key, value):
        self.r_call('hset', key, value)

    def __delitem__(self, key):
        self.r_call('hdel', key)

    def __contains__(self, key):
        return self.r_call('hexists', key)

    def keys(self):
        return self.r_call('hkeys')


class List(RedisDataType):

    def __getitem__(self, key_or_slice):
        if isinstance(key_or_slice, slice):
            data = self.r_call('lrange', key_or_slice.start or 0,
                                         key_or_slice.stop or -1)
        else:
            data = self.r_call('lindex', key_or_slice)
        if data is None:
            raise IndexError('Redis returned None')
        return data

    def __setitem__(self, index, value):
        # from redish
        try:
            self.r_call('lset', index, value)
        except ResponseError, exc:
            if "index out of range" in exc.args:
                raise IndexError("list assignment index out of range")
            raise

    def __len__(self):
        return self.r_call('llen')

    def append(self, value):
        return self.r_call('rpush', value)

    def pop(self, index=None):
        if index is None:
            return self.r_call('rpop')
        if index == 0:
            return self.r_call('lpop')
        raise IndexError('Not supported by Redis')


class Set(RedisDataType):

    def __iter__(self):
        return iter(self.get_set())

    def __len__(self):
        return self.r_call('scard')

    def __contains__(self, value):
        return self.r_call('sismember', value)

    def get_set(self):
        return self.r_call('smembers')

    def add(self, *values):
        self.r_call('sadd', *values)

    def remove(self, value):
        if not self.r_call('remove', value):
            raise KeyError()
