# coding=utf-8
"""Login feature tests."""

from functools import partial
import pytest
import pytest_bdd

scenario = partial(pytest_bdd.scenario, "functional/subpage.feature")


@pytest.mark.nondestructive
@scenario("Visit subpage")
def test_visit_subpage():
    """Login."""


@pytest_bdd.given(pytest_bdd.parsers.parse('I visit the {page} page'))
def visit_example_page(base_selenium, page):
    """Dummy given."""


@pytest_bdd.then(pytest_bdd.parsers.parse('I am on the {page} page'))
def check_example_page_url(base_selenium, base_url, page, page_mappings):
    """ Check page url is corret """
    try:
        from urlparse import urljoin
    except ImportError:
        # python3 compatibility
        from urllib.parse import urljoin
    assert base_selenium.current_url == urljoin(base_url, page)
