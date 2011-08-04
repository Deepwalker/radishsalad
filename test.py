from . import models as m

# models

class User(m.Model):
    name = m.String()
    subscribers = m.Set()
    profile = m.Hash()
    messages = m.List()
    read = m.List()

if __name__ == '__main__':
    u = User('1234')

    u.name = 'Donald'
    assert u.name == 'Donald'

    u.profile['born_at'] = 'London'
    assert dict(u.profile) == {'born_at': 'London'}

    u.messages.clear()
    u.messages.append('My first tweet!!! Im your dark auditor!')
    assert list(u.messages) == ['My first tweet!!! Im your dark auditor!']

    u.subscribers.clear()
    u.subscribers.add('roberto')
    u.subscribers.add('paulo')
    assert 'roberto' in u.subscribers
    assert {'roberto', 'paulo'} == u.subscribers.get_set()
