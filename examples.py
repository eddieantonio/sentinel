#!/usr/bin/env python

import sentinel

"""
TODO: Turn this into test suite.
TODO: pickling test
TODO: copy() and deepcopy() tests
"""

Leaf = sentinel.create('Leaf', extra_methods={
    'is_leaf': property(lambda self: True)
    })

class Node(object):
    def __init__(self, payload, left=Leaf, right=Leaf):
        self.__left = left
        self.__right = right
        # Only non-rewritable attribute.
        self.payload = payload
    left = property(lambda self: self.__left)
    right = property(lambda self: self.__right)
    @property
    def is_leaf(self):
        return False
    def __repr__(self):
        attrs = ('payload', 'left', 'right')
        props = ('%s=%r' % (attr, getattr(self, attr)) for attr in attrs)
        return 'Node(' + ', '.join(props) + ')'

class Maybe(object):
    """
    Ripped off from Haskell, natrually.

    >>> from math import sqrt as _sqrt
    >>> sqrt = lambda x: Nothing if x < 0 else Just(_sqrt(x))
    >>> sqrt(2)
    Just(1.4142135623730951)
    >>> sqrt(-2)
    Nothing
    >>> sqrt(49.0) >> (lambda x: x ** 2)
    Just(49.0)
    >>> a = _
    >>> sqrt(-49.0) >> (lambda x: x ** 2)
    Nothing
    >>> b = _
    >>> a.getOr(0) + b.getOr(0)
    49.0
    """
    @property
    def val(self):
        raise ValueError('Cannot get value of Nothing')

    def __rshift__(self, _func):
        return self

    def getOr(self, substitute=None):
        return substitute

    def getOrElse(self, func):
        return func()

class Just(Maybe):
    def __init__(self, val):
        self.__val = val

    val = property(lambda self: self.__val)

    def __rshift__(self, func):
        return Just(func(self.__val))

    def __repr__(self):
        return 'Just(%r)' % (self.__val,)

    getOr = getOrElse = lambda self, _ignored: self.__val


Nothing = sentinel.create('Nothing', (Maybe,))

AlwaysSmaller = sentinel.create('always smaller', (tuple,), {}, (None, None, None))
