#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import copy
import pickle

import pytest

import sentinel

try:
    import varname  # type: ignore
except ImportError:
    HAS_VARNAME = False
else:
    HAS_VARNAME = True

# Must be defined at module-level due to limitations in how the pickle module works :/
Pickleable = sentinel.create("Pickleable")


def test_basic_usage():
    """
    Tests basic things in the README
    """
    Nothing = sentinel.create("Nothing")
    assert str(Nothing) == repr(Nothing) == "Nothing"

    MissingEntry = sentinel.create("MissingEntry")
    d = {"stdout": None, "stdin": 0}
    assert d.get("stderr", MissingEntry) is MissingEntry


def test_adding_methods():
    """
    From the README -- adding methods to the Leaf singleton.
    """

    def _search_leaf(self, key):
        raise KeyError(key)

    Leaf = sentinel.create(
        "Leaf",
        cls_dict={"search": _search_leaf, "is_leaf": property(lambda self: True)},
    )

    class Node(object):
        is_leaf = False

        def __init__(self, key, payload, left=Leaf, right=Leaf):
            self.left = left
            self.right = right
            self.key = key
            self.payload = payload

        def search(self, key):
            if key < self.key:
                return self.left.search(key)
            elif key > self.key:
                return self.right.search(key)
            else:
                return self.payload

    tree = Node(2, "bar", Node(1, "foo"), Node(3, "baz"))
    assert tree.search(1) == "foo"
    with pytest.raises(KeyError):
        tree.search(4) == "foo"


def test_always_greater():
    """
    From README -- test overriding dunder methods.
    """

    # When I wrote this in 2014 I thought it was a brilliant idea, but now it seems like
    # this hack would probably invalidate assumptions made by a lot of code :/
    IntInfinity = sentinel.create(
        "IntInfinity",
        (int,),
        cls_dict={
            "__lt__": lambda self, other: False,
            "__gt__": lambda self, other: True,
            "__ge__": lambda self, other: True,
            "__le__": lambda self, other: True if self is other else False,
        },
    )

    assert isinstance(IntInfinity, int)
    assert IntInfinity > 10 ** 1000
    assert (10 ** 1000 > IntInfinity) == False

    # uh, okay, this is wild and also bad:
    assert IntInfinity == 0
    assert bool(IntInfinity) == False
    assert IntInfinity + 8 == 8

    # This is less wild but still weird
    arg = (IntInfinity, None, None)
    AlwaysGreater = sentinel.create("AlwaysGreater", (tuple,), {}, arg)
    assert (1, ..., ...) < AlwaysGreater
    assert (AlwaysGreater < (1, ..., ...)) == False


def test_new_returns_singleton():
    """
    Tests that getting the class and calling it returns the same singleton instance.
    """
    ExistingSentinel = sentinel.create("ExistingSentinel")
    Constructor = type(ExistingSentinel)
    assert Constructor() is ExistingSentinel


def test_pickle(tmp_path):
    """
    Save a singleton to a pickle and get it back out.
    """

    # Just put it everywhere:
    arbitrary_data_structure = {Pickleable: (Pickleable, [Pickleable])}

    pickle_path = tmp_path / "data.pickle"
    with pickle_path.open(mode="wb") as fp:
        pickle.dump(arbitrary_data_structure, fp)

    with pickle_path.open(mode="rb") as fp:
        unpickled = pickle.load(fp)

    # Open up the data structure
    assert Pickleable in unpickled
    assert unpickled[Pickleable][0] is Pickleable
    assert unpickled[Pickleable][1][0] is Pickleable


def test_copy():
    """
    Tests that copy.deepcopy() works.
    """
    Copyable = sentinel.create("Copyable")

    arbitrary_data_structure = {Copyable: (Copyable, [Copyable])}

    copied = copy.deepcopy(arbitrary_data_structure)
    assert copied is not arbitrary_data_structure
    assert copied == arbitrary_data_structure

    # Check that the structure is the same
    assert Copyable in copied
    assert copied[Copyable][0] is Copyable
    assert copied[Copyable][1][0] is Copyable
    # Check that the objects are different
    assert copied[Copyable][1] is not arbitrary_data_structure[Copyable][1]


@pytest.mark.skipif(not HAS_VARNAME, reason="varname PyPI package not installed")
def test_varname():
    """
    Tests inferring the variable name. Requires varname library be installed.
    """

    Dark = sentinel.create()
    Magicks = sentinel.create()

    assert repr(Dark) == "Dark"
    assert repr(Magicks) == "Magicks"


def test_can_get_instance_from_class():
    """
    Tests whether you can retrieve the instance from the class.  I literally
    don't remember why this is a feature of this package, but it'll be a
    regression if I remove it, so here we are!
    """
    MySentinel = sentinel.create("MySentinel")
    MySenintelType = type(MySentinel)
    assert MySenintelType.instance is MySentinel
