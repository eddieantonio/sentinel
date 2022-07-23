"""
Create sentinel and singleton objects.

Copyright 2014–2022 © Eddie Antonio Santos. MIT licensed.

With contributions from:
 - Simeon Visser (https://github.com/svisser)
 - WildCard65 (https://github.com/WildCard65)
 - Micael Jarniac (https://github.com/MicaelJarniac)

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import inspect
import typing
from typing import Any, Dict, Optional, Tuple

# sentinel.create() is the only publically-exposed member of this package.
__all__ = ["create"]
__version__ = "1.0.0"

# All instances
_sinstances: Dict[type, object] = {}

# By default, Sentinels inherit from object, but this can be overridden
# (for some reason that I can't remember anymore).
_DEFAULT_MRO = (object,)


@typing.no_type_check
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
    specified (that is, your new sentinel can be a subclass). Provide
    the MRO as tuple of all classes that it inherits from. If only one
    class, provide a 1-tuple: e.g., (Cls,).

    Additionally extra class attributes, such as methods can be provided
    in cls_dict. The following methods are provided, but
    can be overridden:

        __repr__()
            Returns the class name, similar to None and Ellipsis.
        __copy__()
        __deepcopy__()
            Always return the same singleton instance such that
            ``copy(Sentinel) is Sentinel`` is true.
        __reduce__()
            Provides proper pickling prowess. That is,
            ``pickle.loads(pickle.dumps(Sentinel)) is Sentinel`` is
            true.

    Finally, the remaining arguments and keyword arguments are passed to
    the super class's __init__().  This is helpful when for
    instantiating base classes such as if you're extending tuple.
    """

    if name is None:
        try:
            from varname import varname  # type: ignore
        except ImportError as error:
            raise ImportError(
                "Cannot infer variable name without varname library; "
                "please install the varname PyPI package to enable this feature: "
                "pip install sentinel[varname]\n"
            ) from error
        name = varname()

    _cls_dict = {
        # Make the singleton always belong to the module of its caller.
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

    # The sentinel's meta class.
    # Normally, you shouldn't have access to this unless you're being sneaky:
    # >>> MySentinel = sentinel.create("MySentinel")
    # >>> type(type(MySentinel))
    # (don't do this.)
    class _SentinelMeta(
        # Inherit from the base type of the first type:
        type(mro[0])
    ):
        # Allows you to get the singleton instance from the Sentinel's class.
        # >>> type(Sentinel).instance == Sentinel
        # (I have no idea why I though this was necessary).
        instance = property(
            fget=_sinstances.get, doc="""Gets the instance of this sentinel type."""
        )

        # Ensure that every call to the Sentinel's class just returns the singleton
        # instance:
        def __call__(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> object:
            try:
                return _sinstances[self]
            except KeyError:
                # We use super() in case __call__ was overriden:
                instance = super().__call__(*args, **kwargs)
                _sinstances[self] = instance

                return instance

    if cls_dict is not None:
        _cls_dict.update(cls_dict)
    _sentinel = _SentinelMeta("_Sentinel", mro, _cls_dict)

    instance = _sentinel(*args, **kwargs)
    _sentinel.__new__ = _sentinel_failing_new

    return instance


def _get_caller_module() -> Optional[str]:
    """
    Return the module name of the caller of sentinel.create().
    """
    stack = inspect.stack()
    assert len(stack) > 1

    caller = stack[2][0]
    return caller.f_globals.get("__name__")


def _sentinel_failing_new(cls: type, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]):
    """
    Implementation of __new__ that always throws a TypeError.  Sentinels *must* be
    singleton instances, so instantiating a new sentinel with __new__ is a big no-no, so
    we disable it. Don't do it!
    """
    raise TypeError("This sentinel object can not be allocated more than once")
