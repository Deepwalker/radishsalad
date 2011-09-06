RadishSalad
~~~~~~~~~~~

Radishsalad is simple lib for work with redis datastore in more pythonic way.


Base
====

It include String, Hash, List and Set classes, that represent redis datatypes.
You need to initialize datatype with key:

    >>> dt.List('main stream').append('Blogger Navalniy discovered new corruption scheme in Russia!')
    1L
    >>> list(dt.List('main stream'))
    ['Blogger Navalniy discovered new corruption scheme in Russia!']


    >>> up = dt.Hash('0:user profile')
    >>> up['name'] = 'deepwalker'
    >>> dict(up)
    {'name': 'deepwalker'}
    >>> 'name' in up
    True


    >>> friends = dt.Set('friends')
    >>> friends.add(1929340)
    >>> set(friends)
    set(['1929340'])
    >>> 1929340 in friends
    True


Models
======

Radishsalad has `models` module that is not positioned as Django ORM thing. Its just helper
for keys name generation.
So you create an model:

    >>> from radishsalad import models as m
    >>> class User(m.Model):
    ...      name = m.String()
    ...      subscribers = m.Set()
    ...      profile = m.Hash()
    ...      messages = m.List()
    ...      read = m.List()
    ... 

And for using you need initialize it with key:
    
    >>> user = User(1000)

Now you have `user` instance, and you can get keys for it members:

    >>> user.name.get_key()
    'user:1000:name'

Library does not return you a string instead of `String` objects for using in redis.mget:

    >>> from radishsalad.connection import get_redis
    >>> r = get_redis()
    >>> r.mset(dict((User(i).name.get_key(), i) for i in xrange(40)))
    >>> r.mget(User(i).name.get_key() for i in xrange(40))
    ['0', '1', '2', '3', '4', '5', '6', '7', ... '38', '39']


