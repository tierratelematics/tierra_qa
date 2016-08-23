tierra_qa
=========

[![Build Status](https://travis-ci.org/tierratelematics/tierra_qa.svg?branch=master)](https://travis-ci.org/tierratelematics/tierra_qa)

``tierra_qa`` is a package that aims to find a new repeatable pattern for 
black box QA testing applied to any web application.

It is internally based on:
* py.test
* pytest-selenium
* pytest-bdd
* optionally on pytest-docker (TODO)

In the next future we'll provide a generic package generator for easy setup of
testing.

Why py.test
-----------

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
-----------------

Prerequisites:

* python-dev
* virtualenv
* Firefox, Chrome, etc

Clone the ``tierra_qa`` package and run:

    $ python setup.py develop

How to use it
-------------

Once installed you can launch tests with:

    $ py.test --splinter-webdriver=firefox [--base-url http://anotherurl.com/] --credentials="USERID1;USERNAME1;PASSWORD1|..."

With the ``--credentials`` parameter you can specify different multiple user credentials splitted by a | character where:

* USERID1, stands for the user identifier used in test cases
* USERNAME1, stands for the username used for login
* PASSWORD1, password associated to the above username

The USERID1 will be used in order to mark tests if you want an authenticated session, for example::

    import pytest

    @pytest.mark.user('USERID1')
    def test_login(loggedin_browser):
        # you'll have a selenium session authenticated with the USERID1
        assert 1

By default the default ``base_url`` is http://tierratelematics.com/ and it
is specified on ``setup.cfg`` file.
If you provide multiple ``--base-url`` parameters your test suite will be automatically repeated against different environments (using same
credentials).

How to create your own qa package
=================================

Once you have installed ``tierra_qa`` you can create your own package typing the following command:

* tierra_qa_clone YOURPACKAGE_QA
