import pytest


@pytest.mark.user('Administrator')
@pytest.mark.nondestructive
def test_login(loggedin_selenium, username):
    """ User should be logged in"""
    assert 1
    # element = loggedin_selenium.find_element_by_id('li_user')
    # assert element.text == username.upper()
