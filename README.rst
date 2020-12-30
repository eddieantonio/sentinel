*************************************************
sentinel — create sentinel and singleton objects
*************************************************

|Tests| |PyPI version|

.. |Tests| image:: https://github.com/eddieantonio/sentinel/workflows/Python%20package/badge.svg
   :target: https://github.com/eddieantonio/sentinel/actions?query=workflow%3A%22Python+package%22
.. |PyPI version| image:: https://img.shields.io/pypi/v/sentinel
   :target: https://pypi.org/project/sentinel/

Creates simple sentinel objects which are the only instance of their own
anonymous class. As a singleton, there is a guarantee that there will only
ever be one instance: they can be safely used with ``pickle`` and ``cPickle``
alike, as well as being able to be used properly with ``copy.deepcopy()``. In
addition, a self-documenting ``__repr__`` is provided for free!

Usage
=====

Sentinels_ are singleton_ objects that typically represent some end or
terminating condition. Some singletons already exist in Python, like ``None``,
``NotImplemented``, and ``Ellipsis``.


All that's needed to create a sentinel is its name:

>>> import sentinel
>>> Nothing = sentinel.create('Nothing')
>>> Nothing
Nothing

This by itself is useful when other objects such as ``None``, ``False``,
``0``, ``-1``, etc.  are entirely valid values. For example, setting default
values when all other values are valid with: ``dict.setdefault()``:

>>> MissingEntry = sentinel.create('MissingEntry')
>>> d = {'stdout': None, 'stdin': 0, 'EOF': -1}
>>> [d.setdefault(key, MissingEntry) for key in ('stdin', 'stdout', 'stderr')]
[0, None, MissingEntry]

Alternatively, using ``dict.get()`` when fetching values:

>>> d = {'stdout': None, 'stdin': 0, 'EOF': -1}
>>> d.get('stdout', MissingEntry)
None
>>> d.get('stdin', MissingEntry)
0
>>> d.get('stderr', MissingEntry)
MissingEntry

It's known immediately which value was missing from the dictionary in a
self-documenting manner.

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

    $ poetry install

Next, I recommend you do all development tasks within the ``poetry shell``::

    $ poetry shell
    (sentinel-nUnrocCf-py3.9) $ black .
    (sentinel-nUnrocCf-py3.9) $ pytest

.. _Sentinels: http://en.wikipedia.org/wiki/Sentinel_nodes
.. _singleton: http://en.wikipedia.org/wiki/Singleton_pattern
.. _Poetry: https://python-poetry.org/
.. _install poetry: https://python-poetry.org/docs/#installation
