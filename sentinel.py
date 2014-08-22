#!/usr/bin/env python
# coding: utf-8

"""
sentinel -- create sentinel objects.

Copyright 2014 © Eddie Antonio Santos. MIT licensed.
"""

import inspect

__all__ = ['create']
__version__ = '0.1.0'

def get_caller_module():
    """
    Returns the name of the caller's module as a string.

    >>> get_caller_module()
    '__main__'
    """
    stack = inspect.stack()
    assert len(stack) > 1
    caller = stack[2][0]
    return caller.f_globals['__name__']

def create(name, mro=(object,), extra_methods={}, *args, **kwargs):
    """
    create(name, mro=(object,), extra_methods={}, ...) -> Sentinel instance

    Creates a new sentinel instance. This is a singleton instance kind of like
    the builtin None, and Ellipsis.

    """

    cls_dict = {}

    cls_dict.update(
        # Provide a nice, clean, self-documenting __repr__
        __repr__ = lambda self: name,
        # Provide a copy and deepcopy implementation which simply return the
        # same exact instance.
        __deepcopy__ = lambda self, _memo: self,
        __copy__ = lambda self: self,
        # Provide a hook for pickling the sentinel.
        __reduce__ = lambda self: name
    )

    cls_dict.update(extra_methods)

    anon_type = type(name, mro, cls_dict)

    # Stack introspection -- make the singleton always belong to the module of
    # its caller. If we don't do this, pickling using __reduce__() will fail!
    anon_type.__module__ = get_caller_module()

    # Return the singleton instance of this new, "anonymous" type.
    return anon_type(*args, **kwargs)

