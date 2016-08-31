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


try:
    from urlparse import urljoin
except ImportError:
    # python3 compatibility
    from urllib.parse import urljoin

import os
import pytest
try:
    from _pytest.fixtures import FixtureLookupError
except ImportError:
    from _pytest.python import FixtureLookupError

from time import sleep
import tierra_qa



def pytest_addoption(parser):
    # ``py.test --runslow`` causes the entire testsuite to be run, including test
    # that are decorated with ``@@slow`` (scaffolding tests).
    # see http://pytest.org/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option  # noqa
    parser.addoption("--runslow", action="store_true", help="run slow tests")

    # Avoid passwords stored inside the test code
    parser.addoption(
        "--credentials",
        action="store",
        default='',
        help="list of credentials with USERID1;USERNAME1;PASSWORD1|...")


def pytest_runtest_setup(item):
    if 'slow' in item.keywords and not item.config.getoption("--runslow"):
        pytest.skip("need --runslow option to run")


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
def base_browser(base_url, browser, request, page_mappings):
    """ Returns a selenium instance pointing to the base_url (not logged in).
        Optionally base_url + page if available.
    """
    page = None
    try:
        page = request.getfuncargvalue('page')
    except FixtureLookupError:
        pass
    url = base_url
    if page:
        url = urljoin(base_url, page_mappings[page])
    browser.visit(url)
    sleep(2)
    return browser

@pytest.fixture
def loggedin_browser(base_browser, username, password):
    """ Returns a logged in selenium session on the marked user
        for a specific url (but you can override username and
        password fixtures using conftest.py inheritance acquisition).
    """
    # implement here your related login logics
    return base_browser

@pytest.fixture(scope="session")
def splinter_screenshot_dir():
    """Feature files base directory."""
    return os.path.join(os.path.dirname(tierra_qa.__file__), 'screenshots')

@pytest.fixture(scope='session')
def splinter_driver_kwargs(splinter_webdriver):
    """Webdriver kwargs."""
    if splinter_webdriver == 'firefox':
        return {'capabilities':{'marionette':True}}
    return {}
