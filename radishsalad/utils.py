#! /usr/bin/env python


class StringMixin(object):
    # From babel
    def value(self):
        if getattr(self, '_value', None) is None:
            self._value = self.r_call('get') or ''
            if hasattr(self.instance, 'cache'):
                self.instance.cache[self._key] = self._value
        return self._value

    def __contains__(self, key):
        return key in self.value()

    def __nonzero__(self):
        return bool(self.value())

    def __dir__(self):
        return dir(self.value())

    def __iter__(self):
        return iter(self.value())

    def __len__(self):
        return len(self.value())

    def __str__(self):
        return str(self.value())

    def __unicode__(self):
        return unicode(self.value())

    def __add__(self, other):
        return self.value() + other

    def __radd__(self, other):
        return other + self.value()

    def __mod__(self, other):
        return self.value() % other

    def __rmod__(self, other):
        return other % self.value()

    def __mul__(self, other):
        return self.value() * other

    def __rmul__(self, other):
        return other * self.value()

    def __lt__(self, other):
        return self.value() < other

    def __le__(self, other):
        return self.value() <= other

    def __eq__(self, other):
        return self.value() == other

    def __ne__(self, other):
        return self.value() != other

    def __gt__(self, other):
        return self.value() > other

    def __ge__(self, other):
        return self.value() >= other


def ichain(iters):
    for itr in iters:
        for i in itr:
            yield i
