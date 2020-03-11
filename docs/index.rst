Welcome to brunns-matchers's documentation!
===========================================

Various custom `PyHamcrest`_ matchers.

.. _PyHamcrest: https://pyhamcrest.readthedocs.io

.. toctree::
   :maxdepth: 2
   :caption: Contents:

      API <api.rst>

Installation
------------

Install from `Pypi <https://pypi.org/project/brunns-matchers/>`_ as usual, using pip , `tox`_, or ``setup.py``.

.. _tox: https://tox.readthedocs.io

Provided matchers
-----------------

Bytestring
~~~~~~~~~~

* :py:func:`~brunns.matchers.bytestring.contains_bytestring` - match if bytestring contains another.

JSON
~~~~

* :py:func:`~brunns.matchers.data.json_matching` - match JSON string.

Date & time
~~~~~~~~~~~

* :py:func:`~brunns.matchers.datetime.is_weekday` - matches date is it's a weekday.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
