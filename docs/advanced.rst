.. _api-tierra_qa.tests.conftest:

========
Advanced
========

Here you can see the technical documentation.

.. automodule:: tierra_qa.tests.conftest
   :members:
   :member-order: bysource

.. automodule:: tierra_qa.config
   :members:
   :member-order: bysource

.. automodule:: tierra_qa.pages.base
   :members:
   :member-order: bysource


BDD tests examples
==================

Here you can see a BDD test example:

.. include:: ../tierra_qa/features/functional/login.feature
   :literal:

where ``Administrator`` stands for the user id.

You have to provide the Administrator ``username`` and ``password``
providing them in the ``credentials_template.yml``. For example:

.. include:: ../credentials_template.yml
   :literal:

