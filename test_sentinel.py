#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pytest

import sentinel


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


# TODO: test pickling
# TODO: test copy() and deepcopy()
