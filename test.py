from radishsalad.connection import get_redis
from radishsalad import models as m

import attest


# models

class User(m.Model):
    name = m.Index('un') # `un` for search user by name
    subscribers = m.Set()
    profile = m.Hash()
    messages = m.List()
    read = m.List()

base = attest.Tests()

@base.test
def base_test():
    # Base datatypes demo

    # Models demo
    u = User('1234')

    u.name = 'Donald'
    assert str(u.name) == 'Donald'

    assert User.name.get_for('Donald').name == 'Donald'
    assert User.name.get_for('Donald').id == '1234'

    u.profile['born_at'] = 'London'
    assert dict(u.profile) == {'born_at': 'London'}

    u.messages.clear()
    u.messages.append('My first tweet!!! Im your dark auditor!')
    assert list(u.messages) == ['My first tweet!!! Im your dark auditor!']

    u.subscribers.clear()
    u.subscribers.add('roberto')
    u.subscribers.add('paulo')
    assert 'roberto' in u.subscribers
    assert set(['roberto', 'paulo']) == u.subscribers.get_set()

    r = get_redis()
    r.mset(dict(zip(User.name.gen_keys(xrange(40)), xrange(40))))
    users = User.from_seq(xrange(40))
    assert range(40) == [int(str(u.name)) for u in users]


if __name__ == '__main__':
    base.run()
