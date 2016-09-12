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
        try:
            userid = request.getfuncargvalue('user_id')
        except FixtureLookupError:
            userid = None
    return userid and credentials_mapping[userid]['username'] or None


@pytest.fixture
def password(credentials_mapping, request):
    """ Returns the real (overridable) password associated to the user
        marker or fixture """
    if 'user_id' in request.keywords:
        userid = request.keywords['user_id'].args[0]
    else:
        try:
            userid = request.getfuncargvalue('user_id')
        except FixtureLookupError:
            userid = None
    return userid and credentials_mapping[userid]['password'] or None


@pytest.fixture(scope="session")
def page_mappings():
    """ Returns the page mappings for paths and page object
        classes.

        See tierra_qa.config.PAGE_MAPPINGS for further details.
    """
    return tierra_qa.config.PAGE_MAPPINGS


@pytest.fixture
def default_page_class():
    return tierra_qa.pages.BasePage


@pytest.fixture
def page(base_url, browser, request, page_mappings, default_page_class,
         username, password):
    """ Returns a selenium instance pointing to the base_url (not logged in).
        Optionally base_url + page if available.
    """
    page_id = None
    try:
        page_id = request.getfuncargvalue('page_id')
    except FixtureLookupError:
        pass
    url = base_url

    if page_id is None:
        url = base_url
        page_class = default_page_class
    else:
        page_mapping = page_mappings.get(page_id)
        path = page_mapping['path']
        page_class = page_mapping.get('page_class', default_page_class)
        url = urljoin(base_url, path)

    page = page_class(browser, base_url=url)

    # visit url
    page.open()

    # login
    if username and password:
        page.login()

    return page


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
