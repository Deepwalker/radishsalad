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
    ...      name2 = m.Index('un')
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

String
------

Library does not return you a string instance instead of `String` objects, due `String` has `get_key` method,
that can be usefull in pair with redis.mget:

    >>> from radishsalad.connection import get_redis
    >>> r = get_redis()
    >>> r.mset(dict((User(i).name.get_key(), i) for i in xrange(40)))
    >>> r.mget(User(i).name.get_key() for i in xrange(40))
    ['0', '1', '2', '3', '4', '5', '6', '7', ... '38', '39']

Index
-----

In addition we have handy `Index` field. Everytime when save it, you have index record created.
Example:

    >>> u = User(1000)
    >>> u.name2 = 'ronaldinio'

When we save 'ronaldinio' in name2, additional values saved with key 'un:user:ronaldinio' and value '1000'.

    >>> User.name2.get_for('ronaldinio')
    <__main__.User object at 0x7f56b40dc190>
    >>> User.name2.get_for('ronaldinio').id
    '1000'

Call `get_for` method of index attribute return object for given string.

Prefetch
========

Models have special class method for create instances with prefetched String fields
over redis MGET method.

So, example:

    >>> User.from_seq(xrange(40))
    [<__main__.User object at 0x7f745bc72d90>, ...]
    >>> [str(u.name) for u in users]
    ['0', '1', '2', '3', '4', ...]

All `name` attributes fetched with one `mget` call. Most interesting that if we
have more then one `String` attribute, `from_seq` will fetch it all for all ids with
one `mget`.

All data we keep in instance `cache` attribute:

    >>> [u.cache for u in users]
    [{'name': '0'}, {'name': '1'}, {'name': '2'},
