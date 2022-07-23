*************************************************
sentinel — create sentinel and singleton objects
*************************************************

|Tests| |PyPI version|

.. |Tests| image:: https://github.com/eddieantonio/sentinel/workflows/Test%20and%20Lint/badge.svg
   :target: https://github.com/eddieantonio/sentinel/actions?query=workflow%3A%22Test+and+Lint%22
.. |PyPI version| image:: https://img.shields.io/pypi/v/sentinel
   :target: https://pypi.org/project/sentinel/

Creates simple sentinel objects.


Install
=======

Basic features::

   pip install sentinel

with extra magic features powered by python-varname_::

   pip install 'sentinel[varname]'


What is a sentinel?
===================

Sentinels_ are singleton_ objects that typically represent some
terminating (end) condition or have a special, symbolic meaning. Python's built-in
``None`` is a sentinel. Python also has other sentinels like ``NotImplemented`` and
``Ellipsis``.

If you want to create your own sentinels, use this library! Make your calls to
``dict.get()`` more meaningful! You can replace the ``object()`` idiom with a sentinel:

.. code-block:: python

   d = {"a": 1, "b": None}

   # Before sentinel:
   missing = object()
   if d.get("c", missing) is missing:
       ... # do some stuff

   # After sentinel:
   Missing = sentinel.create()
   if d.get("c", Missing) is Missing:
       ... # do some stuff


Features
--------

- sentinels are unique
- sentinels are singletons — the **only** instance of their own anonymous class
- sentinels can be used with ``is`` comparisons
- sentinels can be used with ``pickle``
- sentinels can be used with ``copy.deepcopy``
- you can **add** arbitrary attributes and methods to sentinels
- sentinels have a nice, self-documenting ``__repr__``!


Usage
=====

Create a sentinel:

>>> import sentinel
>>> MySentinel = sentinel.create("MySentinel")
>>> MySentinel
MySentinel

If you have python-varname_ installed, or installed this module using
``pip install 'sentinel[varname]'``, ``sentinel.create()`` can infer the name
from the assignment expression:

.. code-block:: python

   import sentinel

   MySentinel = sentinel.create()

   print(MySentinel)  # prints `MySentinel`


**NOTE**: this will not work in the interactive console!

>>> import sentinel
>>> # Fails because varname can't find the source code for the interactive console!
>>> MySentinel = sentinel.create("MySentinel")

Example
-------

Sentinels are useful when other objects such as ``None``, ``False``,
``0``, ``-1``, are valid values within some data structure. For example, setting
default values when all other values are valid with:
``dict.setdefault()``:

.. code-block:: python

   d = {"stdout": None, "stdin": 0, "EOF": -1}

   MissingEntry = sentinel.create()

   [d.setdefault(key, MissingEntry) for key in ("stdin", "stdout", "stderr")]
   [0, None, MissingEntry]

Alternatively, using ``dict.get()`` when fetching values:

>>> d = {"stdout": None, "stdin": 0, "EOF": -1}
>>> d.get("stdout", MissingEntry)
None
>>> d.get("stdin", MissingEntry)
0
>>> d.get("stderr", MissingEntry)
MissingEntry

Since a new sentinel can never occur in the original dictionary, you can tell which
entries are missing or unset in a dictionary in a self-documenting way:

.. code-block:: python

   Unset = sentinel.create()
   if d.get("stdin", Unset) is Unset:
       stdin = 0  # some reasonable default


Adding extra methods and class attributes
-----------------------------------------

Sentinels may also inherit from base classes, or implement extra methods.

Consider a binary search tree with two kinds of nodes: interior nodes
(``Node``) which contain some payload and leaves (``Leaf``), which simply
terminate traversal.

To create singleton leaf which implements a ``search`` method and an
``is_leaf`` property, you may provide any extra class attributes in the
``cls_dict`` keyword argument. The following is a full example of both
the singleton ``Leaf`` and its ``Node`` counterpart:

.. code-block:: python

    def _search_leaf(self, key):
        raise KeyError(key)

    Leaf = sentinel.create('Leaf', cls_dict={
        'search': _search_leaf,
        'is_leaf': property(lambda self: True)
    })

    class Node(object):
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

        is_leaf = property(lambda: false)

Example usage:

>>> tree = Node(2, 'bar', Node(1, 'foo'), Node(3, 'baz'))
>>> tree.search(1)
'foo'
>>> tree.search(4)
Traceback (most recent call last):
    ...
KeyError: 2


Contributing
============

This project uses Poetry_. To contribute to the codebase, make sure to `install poetry`_,
With Poetry installed, clone then repo, then within the repo directory, install the developer dependencies::

    $ poetry install --extras varname

Next, I recommend you do all development tasks within the ``poetry shell``::

    $ poetry shell
    (sentinel-nUnrocCf-py3.9) $ black .
    (sentinel-nUnrocCf-py3.9) $ pytest

.. _Sentinels: http://en.wikipedia.org/wiki/Sentinel_nodes
.. _singleton: http://en.wikipedia.org/wiki/Singleton_pattern
.. _Poetry: https://python-poetry.org/
.. _install poetry: https://python-poetry.org/docs/#installation
.. _python-varname: https://github.com/pwwang/python-varname
