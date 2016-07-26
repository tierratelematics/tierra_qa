import pytest


@pytest.mark.user('Administrator')
@pytest.mark.nondestructive
def test_login(loggedin_selenium, username):
    """ User should be logged in"""
    # This is an example of a non-BDD test.
    # Implement here your project custom 
    # logics for login check
    assert 1
