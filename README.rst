=========
tierra_qa
=========

.. image:: https://travis-ci.org/tierratelematics/tierra_qa.svg?branch=master
       :target: https://travis-ci.org/tierratelematics/tierra_qa

.. image:: https://requires.io/github/tierratelematics/tierra_qa/requirements.svg?branch=master
       :target: https://requires.io/github/tierratelematics/tierra_qa/requirements/?branch=master

.. image:: https://readthedocs.org/projects/tierra_qa/badge/?version=latest
       :target: http://tierra_qa.readthedocs.io

.. image:: https://codecov.io/gh/tierratelematics/tierra_qa/branch/master/graph/badge.svg
       :target: https://codecov.io/gh/tierratelematics/tierra_qa

.. image:: https://api.codacy.com/project/badge/Grade/0698c7aa2e164ee996518737aad7d6f4
       :target: https://www.codacy.com/app/davide-moro/tierra_qa?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tierratelematics/tierra_qa&amp;utm_campaign=Badge_Grade



``tierra_qa`` is a package that aims to find a new repeatable pattern for 
black box QA testing applied to any web application.

It is internally based on:

* `pytest`_
* `pytest_splinter`_
* `pytest_bdd`_
* `PyPOM`_

Why py.test
===========

``py.test`` is one of the most promising test frameworks built with Python. It is a generic
framework, so it is not bound to the BDD practise.
So if you are going to test a Python based application, you'll have a unique BDD tool
integrated with the unit, integration and functional tests running just only a command.

It provides a clever dependency injection mechanism for fixture creations and its focus is
minimizing the amount of test code, reusability and modularity.

More links:

* http://pytest.org
* https://pytest.org/latest/fixture.html
* https://pytest.org/latest/example/markers.html
* https://pytest.org/latest/example/simple.html

How to install it
=================

Prerequisites:

* python-dev
* virtualenv
* Firefox (requires geckodriver), Chrome, etc

Clone the ``tierra_qa`` package and run::

    $ pip install -r requirements.txt
    $ python setup.py develop

How to use it
=============

Once installed you can launch tests with::

    $ py.test --splinter-webdriver=firefox --variables credentials_template.yml [--base-url http://anotherurl.com/]

With the ``--variables`` parameter you can read user credentials from a YAML file like that::

    credentials:
      USERID1:
        username: USERNAME1
        password: PASSWORD1

where:

* *USERID1*, stands for the user identifier used in test cases
* *USERNAME1*, stands for the username used for login
* *PASSWORD1*, password associated to the above username

The YAML file 'credentials_template.yml' has to be considered only a template for credentials and we
*stronlgy* suggest to do not put credential files under version control.
If you use Travis CI (http://travis-ci.org/) you can encrypt files with sensible information:

* https://docs.travis-ci.com/user/encrypting-files/

By default the default ``base_url`` is http://tierratelematics.com/ and you can change it editing the
``setup.cfg`` file.

How to create your own qa package
=================================

Once you have installed ``tierra_qa`` you can create your own package typing the following command::

    $ tierra_qa_clone YOURPACKAGE_QA

.. include:: ./fixture_diagrams.rst

.. _pytest: http://doc.pytest.org
.. _pytest_splinter: http://pytest-splinter.readthedocs.io
.. _pytest_bdd: http://pytest-bdd.readthedocs.io
.. _PyPOM: http://pypom.readthedocs.io
