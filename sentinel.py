#!/usr/bin/env python
# coding: utf-8

"""
Create sentinel and singleton objects.

Copyright 2014, 2020 © Eddie Antonio Santos. MIT licensed.

With contributions from:
 - Simeon Visser (https://github.com/svisser)
 - WildCard65 (https://github.com/WildCard65)

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import inspect
from typing import Any, Dict, Optional, Tuple

__all__ = ["create"]
__version__ = "0.2.0"

_sinstances: Dict[type, object] = {}

_DEFAULT_MRO = (object,)


def _get_caller_module() -> Optional[str]:
    stack = inspect.stack()
    assert len(stack) > 1

    caller = stack[2][0]
    return caller.f_globals.get("__name__")


def _sentinel_failing_new(cls: type, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]):
    raise TypeError("This sentinel object can not be allocated more than once")


def create(
    name: str = None,
    mro: Tuple[type, ...] = _DEFAULT_MRO,
    cls_dict: Dict[str, Any] = None,
    *args: Tuple[Any, ...],
    **kwargs: Dict[str, Any]
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

    if name is None:
        try:
            from varname import varname  # type: ignore
        except ImportError as error:
            raise ImportError(
                "Cannot infer variable name without varname library; "
                "please install the varname PyPI package to enable this feature: "
                "pip install sentinel[varname]"
            ) from error
        name = varname()

    _cls_dict = {
        # make the singleton always belong to the module of its caller.
        # If we don't do this, pickling using __reduce__() will fail!
        "__module__": _get_caller_module(),
        # Provide a nice, clean, self-documenting __repr__
        "__repr__": lambda _: name,
        # Provide a hook for pickling the sentinel.
        "__reduce__": lambda _: name,
        # Provide a copy and deepcopy implementation which simply return the
        # same exact instance.
        "__copy__": lambda self: self,
        "__deepcopy__": lambda self, _: self,
    }

    if mro == _DEFAULT_MRO:
        # Add an empty slots tuple if we're only inheritting from 'object'
        _cls_dict["__slots__"] = ()
    elif object in mro:
        # Validate if object is the last type in the provided mro list.
        assert mro[-1] is object, "object should ALWAYS the last type in a mro"

    class _SentinelMeta(type(mro[0])):  # Inherit from the base type of the first type.
        instance = property(
            fget=_sinstances.get, doc="""Gets the instance of this sentinel type."""
        )

        def __call__(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> object:
            try:
                return _sinstances[self]
            except KeyError:
                inst = super().__call__(
                    *args, **kwargs
                )  # We use super() incase __call__ was overriden.
                _sinstances[self] = inst

                return inst

    if cls_dict is not None:
        _cls_dict.update(cls_dict)
    _sentinel = _SentinelMeta("_Sentinel", mro, _cls_dict)

    inst = _sentinel(*args, **kwargs)
    _sentinel.__new__ = _sentinel_failing_new

    return inst
