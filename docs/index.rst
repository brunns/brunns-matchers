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

* :py:func:`~brunns.matchers.datetime.is_weekday` - matches date if it's a weekday.

Database
~~~~~~~~

* :py:func:`~brunns.matchers.dbapi.has_table` - matches if database has table.
* :py:func:`~brunns.matchers.dbapi.has_table_with_rows` - matches if database has table with rows matching.

HTML
~~~~

* :py:func:`~brunns.matchers.html.has_title` - matches if HTML has title with content.
* :py:func:`~brunns.matchers.html.has_named_tag` - matches if HTML has tag with name.
* :py:func:`~brunns.matchers.html.has_id_tag` - matches if HTML has tag with id.
* :py:func:`~brunns.matchers.html.tag_has_string` - matches if tag has string.
* :py:func:`~brunns.matchers.html.has_class` - matches if tag has class.
* :py:func:`~brunns.matchers.html.has_table` - matches if HTML has table.
* :py:func:`~brunns.matchers.html.has_row` - matches if table has row.
* :py:func:`~brunns.matchers.html.has_header_row` - matches if table has header row.
* :py:func:`~brunns.matchers.html.has_id` - matches if tag has id.
* :py:func:`~brunns.matchers.html.has_attributes` - matches if tag has attributes.
* :py:func:`~brunns.matchers.html.has_link` - matches if HTML has link.
* :py:func:`~brunns.matchers.html.has_image` - matches if HTML has image.

Matchers
~~~~~~~~

* :py:func:`~brunns.matchers.matcher.mismatches` - matches if matcher mismatches value.
* :py:func:`~brunns.matchers.matcher.mismatches_with` - matches if matcher mismatches value with specific message.
* :py:func:`~brunns.matchers.matcher.matches` - matches if matcher matches value.
* :py:func:`~brunns.matchers.matcher.matches_with` - matches if matcher matches value with specific message.

Meta (auto-matchers)

* :py:class:`~brunns.matchers.meta.BaseAutoMatcher` - dynamically create matchers for classes.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
