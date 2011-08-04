from rmodels import models as m

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
    u.profile['born_at'] = 'London'
    u.messages.append('My first tweet!!! Yeah, man! Im your dark auditor!')
    print list(u.messages)

    assert list(u.messages) == ['My first tweet!!! Yeah, man! Im your dark auditor!']
    assert dict(u.profile) == {'born_at': 'London'}
    assert u.name == 'Donald'
