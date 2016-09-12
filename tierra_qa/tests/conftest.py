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
    # ``py.test --runslow`` causes the entire testsuite to be run, including
    # test that are decorated with ``@@slow`` (scaffolding tests).
    # see http://pytest.org/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option  # noqa
    parser.addoption("--runslow", action="store_true", help="run slow tests")


def pytest_runtest_setup(item):
    if 'slow' in item.keywords and not item.config.getoption("--runslow"):
        pytest.skip("need --runslow option to run")


@pytest.fixture
def pytestbdd_feature_base_dir():
    """Feature files base directory."""
    return os.path.join(os.path.dirname(tierra_qa.__file__), 'features')


@pytest.fixture(scope='session')
def credentials_mapping(request, variables):
    """
       This fixture provides users credentials via a file specified on the
       --variables option.The file format is one supported by pytest-variables.

       On the test side you just have to add a marker where you specify
       the user identifier you want to operate with.

       For example::
         import pytest

         @pytest.mark.user_id('USERID1')
         def test_login(loggedin_selenium):
           # you'll have a selenium session authenticated with the USERID1
           assert 1

    """

    return variables['credentials']


@pytest.fixture
def username(credentials_mapping, request):
    """ Returns the real (overridable) username associated to the user
         marker or fixture """

    if 'user_id' in request.keywords:
        userid = request.keywords['user_id'].args[0]
    else:
        userid = request.getfixturevalue('user_id')
    return credentials_mapping[userid]['username']


@pytest.fixture
def password(credentials_mapping, request):
    """ Returns the real (overridable) password associated to the user
        marker or fixture """
    if 'user_id' in request.keywords:
        userid = request.keywords['user_id'].args[0]
    else:
        userid = request.getfuncargvalue('user_id')
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
        return {'capabilities': {'marionette': True}}
    return {}
