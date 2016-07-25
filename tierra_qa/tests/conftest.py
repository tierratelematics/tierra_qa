"""

TODO: add documentation for fixture dependencies

Fixture dependencies
--------------------
.. graphviz::
   digraph tierra_qa_fixtures {
      "allwarnings";
      "app" -> "webtest";
      "config" -> "db_session";
      "config" -> "depot_tween";
      "config" -> "dummy_request";
      "config" -> "events";
      "config" -> "workflow";
      "connection" -> "content";
      "connection" -> "db_session";
      "content" -> "db_session";
      "custom_settings" -> "connection";
      "custom_settings" -> "unresolved_settings";
      "db_session" -> "app";
      "db_session" -> "browser";
      "db_session" -> "filedepot";
      "db_session" -> "root";
      "depot_tween" -> "webtest";
      "dummy_mailer" -> "app";
      "dummy_mailer";
      "dummy_request" -> "depot_tween";
      "events" -> "app";
      "depot_tween" -> "filedepot";
      "depot_tween" -> "mock_filedepot";
      "mock_filedepot";
      "depot_tween" -> "no_filedepots";
      "settings" -> "config";
      "settings" -> "content";
      "setup_app" -> "app";
      "setup_app" -> "browser";
      "unresolved_settings" -> "settings";
      "unresolved_settings" -> "setup_app";
      "workflow" -> "app";
   }
"""

import urlparse
import os
import pytest
import pytest
from _pytest import python
from time import sleep
import tierra_qa


def pytest_addoption(parser):
    """ Avoid passwords stored
        inside the test code
    """
    parser.addoption("--credentials",
                     action="store",
                     default='',
                     help="list of credentials with USERID1;USERNAME1;PASSWORD1|...")

@pytest.fixture
def pytestbdd_feature_base_dir():
    """Feature files base directory."""
    return os.path.join(os.path.dirname(tierra_qa.__file__), 'features')


@pytest.fixture(scope='session')
def credentials_mapping(request):
    """ 
        This fixture provides a mapping of easy to remember user identifiers
        with usernames depending on the --credentials parameter with
        with USERID1;USERNAME1;PASSWORD1|... format and returns something like that::

            {
                'USERID1': {'username':'USERNAME1', 'password': 'PASSWORD1'},
                'USERID2': {'username':'USERNAME2', 'password': 'PASSWORD2'},
            }

        On the test side you just have to add a marker where you specify the
        user identifier you want to operate with.

        For example::
            import pytest

            @pytest.mark.user('USERID1')
            @pytest.mark.nondestructive
            def test_login(loggedin_selenium):
                # you'll have a selenium session authenticated with the USERID1
                assert 1

    """
    credentials = {}
    raw_credentials = request.config.getoption('--credentials')

    for users_info in raw_credentials.split('|'):
        userid, username, password = users_info.split(';', 3)
        credentials[userid] = {'username': username, 'password': password}

    return credentials


@pytest.fixture
def username(credentials_mapping, request):
    """ Returns the real (overridable) username associated to the user marker or fixture """
    if 'user' in request.keywords:
        userid = request.keywords['user'].args[0]
    else:
        userid = request.getfuncargvalue('user')
    return credentials_mapping[userid]['username']

@pytest.fixture
def password(credentials_mapping, request):
    """ Returns the real (overridable) password associated to the user marker or fixture """
    if 'user' in request.keywords:
        userid = request.keywords['user'].args[0]
    else:
        userid = request.getfuncargvalue('user')
    return credentials_mapping[userid]['password']

@pytest.fixture(scope="session")
def page_mappings():
    """ Returns the page mappings, for example:

            {'HomePage': '/', 'HelloPage': '/hello'}

        This way your BDD tests won't refer to the
        suburl that might change, you'll refer to page
        labels instead.
    """
    return tierra_qa.config.PAGE_MAPPINGS

@pytest.fixture
def base_selenium(base_url, selenium, request, page_mappings):
    """ Returns a selenium instance pointing to the base_url (not logged in).
        Optionally base_url + page if available.
    """
    page = None
    try:
        page = request.getfuncargvalue('page')
    except python.FixtureLookupError:
        pass
    url = base_url
    if page:
        url = urlparse.urljoin(base_url, page_mappings[page])
    selenium.get(url)
    sleep(2)
    return selenium

@pytest.fixture
def loggedin_selenium(base_selenium, username, password):
    """ Returns a logged in selenium session on the marked user
        for a specific url (but you can override username and
        password fixtures using conftest.py inheritance acquisition).
    """
#    # fill in username and password
#    username_field = base_selenium.find_element_by_id('txtUsr')
#    password_field = base_selenium.find_element_by_id('txtPwd')
#
#    username_field.send_keys(username)
#    password_field.send_keys(password)
#
#    # submit
#    submit_field = base_selenium.find_element_by_id('btnLogin')
#    submit_field.click()
#    sleep(3)
#
    return base_selenium
