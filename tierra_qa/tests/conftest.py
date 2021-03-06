"""
Fixture Diagrams
----------------

The following diagram shows the interactions between the `pytest fixtures`_
created in the ``tierra_qa`` package:

.. graphviz::

   digraph {
      skin;
      page_mappings,
      request;
      request -> {skin};
   }


.. _pytest fixtures: http://doc.pytest.org/en/latest/fixture.html
"""

import os

import pytest

import tierra_qa
from tierra_qa.config import DEFAULT_PAGES


@pytest.fixture
def pytestbdd_feature_base_dir():
    """Feature files base directory."""
    return os.path.join(os.path.dirname(tierra_qa.__file__), 'features')


@pytest.fixture(scope='session', params=DEFAULT_PAGES.keys())
def skin(request):
    """ This fixture provides the skin associated with the application
        on which starts the test session.
    """
    return request.param


@pytest.fixture(scope="session")
def default_pages():
    """ A mapping with the default page object class for each skin

        It's up to you override this fixture with your settings.

        For example::

            DEFAULT_PAGES = {
                'skin1': 'mypackage.pages.BasePage',
            }
    """
    return {'skin1': 'tierra_qa.pages.BasePage'}


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
