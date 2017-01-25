"""
Fixture Diagrams
----------------

The following diagram shows the interactions between the `pytest fixtures`_
created in the ``tierra_qa`` package:

.. graphviz::

   digraph {
      credentials_mapping;
      skin;
      base_url;
      page_mappings,
      default_page_class;
      base_page;
      page_instance;
      navigation;
      navigation_class;
      skip_by_skin_names;
      variables [color="grey"];
      request [color="grey"];
      browser [color="grey"];
      skin -> {credentials_mapping base_url default_page_class navigation
               skip_by_skin_names};
      variables -> {credentials_mapping base_url} [color="grey"];
      request -> {skin skip_by_skin_names} [color="grey"];
      page_mappings -> {default_page_class base_page navigation}
      base_url -> {base_page navigation};
      browser -> {base_page} [color="grey"];
      default_page_class -> {base_page navigation};
      base_page -> {page_instance};
      navigation_class -> {navigation};
      page_instance -> {navigation};
      credentials_mapping -> {navigation};
   }


.. _pytest fixtures: http://doc.pytest.org/en/latest/fixture.html
"""

import os

import pytest

import tierra_qa
from tierra_qa.util import (
    get_page_class,
    page_factory,
)
from tierra_qa.navigation import Navigation


def pytest_addoption(parser):
    # ``py.test --framework`` causes the entire testsuite to be run, including
    # test that are decorated with ``@@framework`` (scaffolding tests).
    # see http://pytest.org/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option  # noqa
    parser.addoption("--framework", action="store_true",
                     help="run framework tests")


def pytest_runtest_setup(item):
    if 'framework' in item.keywords and \
            not item.config.getoption("--framework"):
        pytest.skip("need --framework option to run")


@pytest.fixture
def pytestbdd_feature_base_dir():
    """Feature files base directory."""
    return os.path.join(os.path.dirname(tierra_qa.__file__), 'features')


@pytest.fixture(scope='session')
def credentials_mapping(skin, variables):
    """
        This fixture provides users credentials via a file specified on the
        --variables option.The file format is one supported by
        pytest-variables.

        :return: credentials mapping dictionary with all available credentials
        :rtype: dict
        :raises: KeyError
    """
    return variables['skins'][skin]['credentials']


@pytest.fixture(scope='session', params=tierra_qa.config.DEFAULT_PAGES.keys())
def skin(request):
    """ This fixture provides the skin associated with the application
        on which starts the test session.
    """
    return request.param


@pytest.fixture(scope='session')
def base_url(skin, variables):
    """ Returns the base_url associated to the skin.
    """
    return variables['skins'][skin]['base_url']


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
def default_page_class(skin, page_mappings):
    """
        Returns the default page object base class.

        :return: base page object class
        :rtype: :py:class:`tierra_qa.pages.BasePage`
    """
    return get_page_class(
        skin,
        page_mappings,
    )


@pytest.fixture
def base_page(base_url, browser, default_page_class, page_mappings):
    """ Base page instance """
    page = page_factory(
        base_url,
        browser,
        default_page_class,
        page_mappings)

    # visit target url
    page.open()

    return page


@pytest.fixture
def page_instance(base_page):
    """ Initialize base page.
        You can override this fixture in order to customize
        the page initialization (eg: some sites needs auth
        after, other sites before)
    """

    # maximize window
    base_page.driver.driver.maximize_window()

    return base_page


@pytest.fixture
def navigation(navigation_class,
               page_instance,
               default_page_class,
               page_mappings,
               credentials_mapping,
               skin,
               base_url):
    """ Wraps a page and a page mappings accessible by
        pages.

        ``navigation.page`` is meant to be mutable since
        through the BDD steps the page instance could
        change.
    """
    nav = navigation_class(
        page_instance,
        default_page_class,
        page_mappings,
        credentials_mapping,
        skin,
        base_url)
    return nav


@pytest.fixture
def navigation_class():
    """ Returns the navigation class used for wrap pages"""

    return Navigation


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


@pytest.fixture(autouse=True)
def skip_by_skin_names(request, skin):
    """ Skip by skin name.

        We support validation for multi skin applications providing the best
        page object class match.

        We expect many failures we want to avoid because many tests will fail
        because the related page object implementation still not exists.

        If you want you can omit a test execution for a given skin adding a
        a ```@pytest.mark.skip_skins(['skin2'])``` decorator on your tests.

        Tests marked with a skin2 skip will be executed for all skins
        except for skin2.

        See http://bit.ly/2dYnOSv for further info.
    """
    if request.node.get_marker('skip_skins'):
        if skin in request.node.get_marker('skip_skins').args[0]:
            pytest.skip('skipped on this skin: {}'.format(skin))
