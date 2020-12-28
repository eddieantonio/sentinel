#!/usr/bin/env python
# coding: utf-8

"""
Create sentinel and singleton objects.

 Copyright 2014 © Eddie Antonio Santos. MIT licensed.

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

import inspect
from typing import Dict, Tuple, Optional, Any

__all__ = ['create']
__version__ = '0.1.3'

class _SentinelMeta(type):
    def __call__(cls, *args:Tuple[Any], **kwargs:Dict[str, Any]) -> object:
        inst = _sinstances.get(cls)
        if inst is None:
            inst = type.__call__(cls, *args, **kwargs)
            _sinstances[cls] = inst

        return inst

_sinstances: Dict[_SentinelMeta, object] = {}
_SentinelMeta.instance = property(fget=_sinstances.get, doc="""Gets the instance of this sentinel type""")

__mro_immortal = (object, )
# pylint: disable=invalid-name
__cls_meta_immortal = _SentinelMeta
# pylint: enable=invalid-name

def _get_caller_module() -> Optional[str]:
    stack = inspect.stack()
    assert len(stack) > 1

    caller = stack[2][0]
    return caller.f_globals.get('__name__')

def _sentinel_failing_new(cls:_SentinelMeta, *args:Tuple[Any], **kwargs:Dict[str, Any]):
    raise TypeError('This sentinel object can not be allocated more than once')

def create(
    name:str, mro:Tuple[type]=__mro_immortal, cls_dict:Dict[str, Any]=None, *args:Tuple[Any], **kwargs:Dict[str, Any]
    ) -> object:
    """
    create(name, mro=(object,), cls_dict=None, ...) -> Sentinel instance

    Creates a new sentinel instance. This is a singleton instance kind
    of like the builtin None, and Ellipsis.

    Method resolution order (MRO) for the anonymous class can be
    specified (i.e., it can be a subclass). Provide the mro as tuple of
    all classes that it inherits from. If only one class, provide a
    1-tuple: e.g., (Cls,).

    Additionally extra class attributes, such as methods can be provided
    in the cls_dict dict. The following methods are provided, but
    can be overridden:

        __repr__()
            Returns the class name, similar to None and Ellipsis.
        __copy__()
        __deepcopy__()
            Always return the same singleton instance such that
            ``copy(Sentinel) is Sentinel`` is true.
        __reduce__()
            Provided for proper pickling prowess. That is,
            ``pickle.loads(pickle.dumps(Sentinel)) is Sentinel`` is
            true.

    Finally, the remain arguments and keyword arguments are passed to
    the super class's __init__().  This is helpful when for
    instantiating base classes such as a tuple.
    """

    _cls_dict = {
        '__module__': _get_caller_module(),
        '__repr__': lambda _: name,
        '__reduce__': lambda _: name,
        '__copy__': lambda self: self,
        '__deepcopy__': lambda self, _: self
    }
    if mro == __mro_immortal:
        mro = ()
        _cls_dict['__slots__'] = ()
    elif object in mro:
        assert mro[-1] is object # object is ALWAYS the last type in a mro
        mro = mro[:-1] # Slice off object from the mro list

    cls_type = __cls_meta_immortal
    for tp in mro:
        # pylint: disable=unidiomatic-typecheck
        if type(tp) is not type:
            # pylint: disable=inconsistent-mro
            class _SentinelMeta(type(tp), __cls_meta_immortal):
                pass

            cls_type = _SentinelMeta
            break
        # pylint: enable=inconsistent-mro, unidiomatic-typecheck

    if cls_dict is not None:
        _cls_dict.update(cls_dict)
    _sentinel = cls_type('_Sentinel', mro, _cls_dict)

    inst = _sentinel(*args, **kwargs)
    _sentinel.__new__ = _sentinel_failing_new

    return inst
