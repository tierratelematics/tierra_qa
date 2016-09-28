# coding=utf-8
"""
    functional's conftest module.

    Here you can place your *common* steps definition if they
    are meant to be shared with different steps and reused.

    You could organize your tests in modules, each of them with
    a conftest.py module in order to create a scope hieararchy.
"""

try:
    from urlparse import urljoin
except ImportError:
    # python3 compatibility
    from urllib.parse import urljoin

import pytest_bdd


@pytest_bdd.given(pytest_bdd.parsers.parse('I am logged in as {user_id}'))
def i_am_loggedin_given(user_id, page):
    """Logged in fixture"""


@pytest_bdd.then('I am logged in')
def check_loggedin_then(page, username):
    """Assert user is logged in. Implement here your
       project related login logics.
    """
    assert 1


@pytest_bdd.when(pytest_bdd.parsers.parse(
    'I visit the {page_id_nofollow} page'))
def visit_example_page(page, page_id_nofollow, page_mappings, base_url):
    """Dummy given."""
    url = urljoin(base_url,
                  page_mappings[page_id_nofollow]['path'])
    page.driver.visit(url)


@pytest_bdd.then(pytest_bdd.parsers.parse(
    'I land on the {page_id_nofollow} page'))
def check_example_page_url(page, base_url, page_id_nofollow, page_mappings):
    """ Check page url matches """
    assert page.current_url == urljoin(base_url,
                                       page_mappings[page_id_nofollow]['path'])
