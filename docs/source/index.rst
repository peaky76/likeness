.. likeness documentation master file, created by
   sphinx-quickstart on Wed Feb 14 22:08:53 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

likeness
========

You want to compare two instances of a class. But standard comparison with ``=``, ``>`` and ``<`` don't achieve what you need.
What you'd like is a numeric value to represent how similar one instance is to another, based on the instance's attributes.
This is what ``likeness`` does. Via a few simple steps, you can compare instances of the same class like this:

.. code-block:: python
   
   a.like(b)


and get a float value ``0 < x < 1`` in return

Quickstart
==========

To make a class comparable in this way, first make it inherit from ``likeness.LikenessMixin``. 

Then, define a class variable ``_likeness_functions``. This should be a dictionary, where the keys are the names of instance attributes, 
and the values are callables analysing those attributes. Each callable should return a float between 0 and 1. And that's it.

You can then compare two objects of this class by calling the ``like`` method on one of them, passing the other as an argument.
The ``LikenessMixin`` will evaluate each of the ``_likeness_functions`` and return the product.

Example
=======

.. code-block:: python

   import operator
   from likeness import ignore, LikenessMixin

   class Person(LikenessMixin):
      _likeness_functions = {
         'name': ignore,
         'sex': operator.eq,
         'age': lambda x, y: 1 - abs(x - y) / 100
      }

      def __init__(self, *, name, sex, age):
            self.name = name
            self.sex = sex
            self.age = age


   a = Person(name='Alice', sex='F', age=40)
   b = Person(name='Betty', sex='F', age=90)


The ``Person`` class is now comparable. ``a.like(b)`` will be calculated as follows:

- ``ignore`` is a simple utility function to indicate you want to ignore this attribute. It always returns 1 so has no effect on output. You don't need to use it, but is a convenient way to self-document.
- ``operator.eq`` is the built-in function that returns 1 if the two values are equal, 0 otherwise, so in this case will also return 1.
- for ``age``, we are using a lambda. This needs two arguments and returns a float between 0 and 1. In this case, it returns 0.5.

Therefore, ``a.like(b)`` will return 1 * 1 * 0.5 = 0.5.

Other utilities
===============

You have seen ``ignore`` already. There are a few other convenience utilities provided:

- ``discount`` - this makes calculations like the one used in ``age`` slightly more convenient. You specify the discount factor which will take the likeness down from 1 to 0. In this case we could replace our lambda with ``discount( abs(x - y) / 100)``.

- ``likeness`` - if one of your attributes is of a type that itself is comparable, you can use this to compare the two instances. 
  For example, if ``Person`` had a ``mother`` attribute, you could use ``likeness`` to compare the two mothers, instead of having to use ``lambda x, y: x.like(y)``

Further info
============

See :doc:`api` for more information.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Home <self>
   api

Indices
=======

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
