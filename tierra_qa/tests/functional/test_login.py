# coding=utf-8
"""Login feature tests."""

from functools import partial
import pytest_bdd


scenario = partial(pytest_bdd.scenario, "functional/login.feature")


@scenario("Successful login")
def test_successfull_login():
    """Login."""
