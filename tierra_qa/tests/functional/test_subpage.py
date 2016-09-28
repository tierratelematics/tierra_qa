# coding=utf-8
"""Login feature tests."""

from functools import partial
import pytest_bdd

scenario = partial(pytest_bdd.scenario, "functional/subpage.feature")


@scenario("Visit subpage")
def test_visit_subpage():
    """Login."""
