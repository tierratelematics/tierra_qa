# coding=utf-8
"""Login feature tests."""

from functools import partial
import pytest_bdd


scenario = partial(pytest_bdd.scenario, "functional/login.feature")


@scenario("Successful login")
def test_successfull_login():
    """Login."""


@pytest_bdd.given(pytest_bdd.parsers.parse('When I log in as {user}'))
def i_am_loggedin_given(user, loggedin_browser):
    """Logged in fixture"""


@pytest_bdd.then('I am logged in')
def check_loggedin_then(loggedin_browser, username):
    """Assert user is logged in. Implement here your
       project related login logics.
    """
    assert 1
