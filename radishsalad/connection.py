#! /user/bin/env python

import redis

class ConnectionSettings(object):
    connector = None

    @classmethod
    def set_connector(cls, connector):
        cls.connector = connector

    @classmethod
    def default_connector(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = redis.Redis()
        return cls.instance

    @classmethod
    def get_connector(cls):
        return cls.connector or cls.default_connector


def get_redis():
    return ConnectionSettings.get_connector()()

