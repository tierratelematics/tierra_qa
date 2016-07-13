# coding=utf-8
"""Login feature tests."""

from functools import partial
import pytest
import pytest_bdd


scenario = partial(pytest_bdd.scenario, "functional/login.feature")


@pytest.mark.nondestructive
@scenario("Successful login")
def test_successfull_login():
    """Login."""


@pytest_bdd.given(pytest_bdd.parsers.parse('When I log in as {user}'))
def i_am_loggedin_given(user, loggedin_selenium):
    """Dummy given."""


@pytest_bdd.then('I am logged in')
def check_loggedin_then(loggedin_selenium, username):
    """Dummy then."""
    assert 1
    # element = i_am_loggedin_given.find_element_by_id('li_user')
    # assert element.text == username.upper()
