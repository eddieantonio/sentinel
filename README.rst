=======================================================
sentinel -- create sentinel nodes and singleton objects
=======================================================

Creates simple sentinel objects which are the only instance of their own
anonymous class. As a singleton, there is a guarentee that there will only
ever be one instance: they can be safely used with ``pickle`` and ``cPickle``
alike, as well as being able to be used properly with ``copy.deepcopy()``. In
addition, a self-documenting ``__repr__`` is provided for free!

Usage
-----

Sentinels_ are singleton_ objects that typically represent some end or
terminating condition. Some singletons already exist in Python, like ``None``
and ``Ellipsis``.


All that's needed to create a sentinel is its name::

    >>> import sentinel
    >>> Nothing = sentinel.create('Nothing')
    >>> Nothing
    Nothing

This by itself is useful when other objects such as ``None``, ``False``,
``0``, ``-1``, etc.  are entirely valid values. For example, setting default
values when all other values are valid with: ``dict.setdefault()``::

    >>> MissingEntry = sentinel.create('MissingEntry')
    >>> d = {'stdout': None, 'stdin': 0, 'EOF': -1}
    >>> [d.setdefault(key, MissingEntry) for key in ('stdin', 'stdout', 'stderr')]
    [0, None, MissingEntry]

Alternativly, using ``dict.get()`` when fetching values::

    >>> d = {'stdout': None, 'stdin': 0, 'EOF': -1}
    >>> d.get('stdout', MissingEntry)
    None
    >>> d.get('stdin', MissingEntry)
    0
    >>> d.get('stderr', MissingEntry)
    MissingEntry

It's known immediately which values was missing from the dictionary in a
self-documenting manner.

Advanced Usage
--------------

Sentinels may also inherit from base classes, or implement extra methods.

Consider a binary tree with two kinds of nodes: interior nodes (``Node``)
which contain some payload and leaves (``Leaf``), which simply terminate
traversal.

To create singleton leaf which implements a ``search`` method and an
``is_leaf`` property, you may provide any extra class attributes in the
**``extra_methods``** keyword argument::

    def _search_leaf(self, key):
        raise KeyError(key)

    Leaf = sentinel.create('Leaf', extra_methods={
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
            if key < self.__key:
                return self.left.search(key)
            elif key > self.key:
                return self.right.search(key)
            else:
                return self.payload

        is_leaf = property(lambda: false)

.. _Sentinels: http://en.wikipedia.org/wiki/Sentinel_nodes
.. _singleton: http://en.wikipedia.org/wiki/Singleton_pattern

