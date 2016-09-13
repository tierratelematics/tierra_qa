# coding=utf-8
"""Login feature tests."""

from functools import partial
import pytest_bdd

scenario = partial(pytest_bdd.scenario, "functional/subpage.feature")


@scenario("Visit subpage")
def test_visit_subpage():
    """Login."""


@pytest_bdd.given(pytest_bdd.parsers.parse('I visit the {page_id} page'))
def visit_example_page(page, page_id):
    """Dummy given."""


@pytest_bdd.then(pytest_bdd.parsers.parse('I am on the {page_id} page'))
def check_example_page_url(page, base_url, page_id, page_mappings):
    """ Check page url is corret """
    try:
        from urlparse import urljoin
    except ImportError:
        # python3 compatibility
        from urllib.parse import urljoin

    assert page.current_url == urljoin(base_url,
                                       page_mappings[page_id]['path'])
