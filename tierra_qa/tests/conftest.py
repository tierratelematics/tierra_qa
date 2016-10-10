"""
Fixture Diagrams
----------------

The following diagram shows the interactions between the `pytest fixtures`_
created in the ``tierra_qa`` package:

.. graphviz::

   digraph {
      base_url [color="grey"];
      browser [color="grey"];
      request [color="grey"];
      base_url -> {page} [color="grey"];
      browser -> {page} [color="grey"];
      request -> {page credentials_mapping username password} [color="grey"];
      credentials_mapping -> {username password}
      username -> {page};
      password -> {page};
      page_mappings -> {page};
      default_page_class -> {page};
   }


.. _pytest fixtures: http://doc.pytest.org/en/latest/fixture.html
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
        --variables option.The file format is one supported by
        pytest-variables.

        :return: credentials mapping dictionary with all available credentials
        :rtype: dict
        :raises: KeyError
    """

    return variables['credentials']


@pytest.fixture
def username(credentials_mapping, request):
    """ Returns the username associated to the user
        marker or in BDD tests.

        :return: username used in login
        :rtype: str
        :raises: KeyError
    """

    if 'user_id' in request.keywords:
        userid = request.keywords['user_id'].args[0]
    else:
        try:
            userid = request.getfixturevalue('user_id')
        except FixtureLookupError:
            userid = None
    return userid and credentials_mapping[userid]['username'] or None


@pytest.fixture
def password(credentials_mapping, request):
    """ Returns the password associated to the user
        marker or in BDD tests.

        :return: password used in login
        :rtype: str
        :raises: KeyError
    """
    if 'user_id' in request.keywords:
        userid = request.keywords['user_id'].args[0]
    else:
        try:
            userid = request.getfixturevalue('user_id')
        except FixtureLookupError:
            userid = None
    return userid and credentials_mapping[userid]['password'] or None


@pytest.fixture(scope="session")
def page_mappings():
    """
        Returns the page mappings dictionary with all known page with:

        * paths
        * optional page object class (otherwise the default implementation
          will be used as fallback provided by :py:func:`default_page_class`)

        See :py:mod:`tierra_qa.config` for further details.

        :return: dictionary with all known pages
        :rtype: dict`
    """
    return tierra_qa.config.PAGE_MAPPINGS


@pytest.fixture
def default_page_class():
    """
        Returns the default page object base class.

        :return: base page object class
        :rtype: :py:class:`tierra_qa.pages.BasePage`
    """
    return tierra_qa.pages.BasePage


@pytest.fixture
def page(base_url, browser, request, page_mappings, default_page_class,
         username, password):
    """
        Returns a page object instance for the ``page_id`` provided in
        BDD parameters that wraps a Splinter driver.

        Optionally the splinter driver might be authenticated, if you
        provides a ``user_id`` parameter in your BDD file.

        The page class depends on your page class mappings:

        * :py:class:`tierra_qa.pages.BasePage` as fallback class
        * whatever you want if you provide something different in
          :py:mod:`tierra_qa.config`'s ``PAGE_MAPPINGS`` dict returned by
          the :py:func:`page_mappings` fixture

        Optionally the Splinter driver will point to the ``base_url`` option
        you provide in configuration files or through command line.

        If this fixture does not fit your needs you can override it
        placing another ``page`` fixture on your own ``conftest.py`` module.

        :return: base page object instance
        :rtype: :py:class:`tierra_qa.pages.BasePage`
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

    # login
    if username and password:
        page.login(username, password)

    # visit url
    page.open()

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
