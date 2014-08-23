======================================================
sentinel ­ create sentinel nodes and singleton objects
======================================================

Creates simple sentinel objects which are the only instance of their own
anonymous class. As a singleton, there is a guarantee that there will only
ever be one instance: they can be safely used with ``pickle`` and ``cPickle``
alike, as well as being able to be used properly with ``copy.deepcopy()``. In
addition, a self-documenting ``__repr__`` is provided for free!

Usage
-----

Sentinels_ are singleton_ objects that typically represent some end or
terminating condition. Some singletons already exist in Python, like ``None``
``NotImplemented``, and ``Ellipsis``.


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

Alternatively, using ``dict.get()`` when fetching values::

    >>> d = {'stdout': None, 'stdin': 0, 'EOF': -1}
    >>> d.get('stdout', MissingEntry)
    None
    >>> d.get('stdin', MissingEntry)
    0
    >>> d.get('stderr', MissingEntry)
    MissingEntry

It's known immediately which value was missing from the dictionary in a
self-documenting manner.

Advanced Usage
--------------

Sentinels may also inherit from base classes, or implement extra methods.

Consider a binary search tree with two kinds of nodes: interior nodes
(``Node``) which contain some payload and leaves (``Leaf``), which simply
terminate traversal.

To create singleton leaf which implements a ``search`` method and an
``is_leaf`` property, you may provide any extra class attributes in the
``extra_methods`` keyword argument. The following is a full example of both
the singleton ``Leaf`` and its ``Node`` counterpart::

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

Example usage::

    >>> tree = Node(2, 'bar', Node(1, 'foo'), Node(3, 'baz'))
    >>> tree.search(1)
    'foo'
    >>> tree.search(4)
    Traceback (most recent call last):
        ...
    KeyError: 2

Advanced usage 2
----------------

Another usage is inheriting from a tuple, in order to do tuple comparison. For
example, consider a scenario where a certain order must be maintained, but
ordering matters. If the key being used to sort is an integer, a plain
``object`` instance will always sort greater::

    >>> (1, ..., ...) < (object(), None, None)
    True

Now say we want to encode this in a neat, self-documenting package. This is
can be done by create a sentinel that inherits from ``tuple`` and is
instantiated with the given tuple::

    arg = (object(), None, None)
    AlwaysGreater = sentinel.create('AlwaysGreater', (tuple,), {}, args)

This will call ``tuple((object(), None, None))``. This means the singleton
will now behave exactly as expected::

    >>> (1, ..., ...) < AlwaysGreater
    True

.. _Sentinels: http://en.wikipedia.org/wiki/Sentinel_nodes
.. _singleton: http://en.wikipedia.org/wiki/Singleton_pattern

