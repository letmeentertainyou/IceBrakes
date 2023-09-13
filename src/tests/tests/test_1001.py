#!/bin/python3
'''Execute pytest_runner on predefined tests and test the exit codes.'''
from src.tests.tools import pytest_runner


def test_exit_0() -> None:
    '''Checks for exit code 0 by running an existing code.'''
    exit_code = pytest_runner('0', get_code=True)   # This test gives exit 0.
    assert exit_code == 0

def test_exit_1() -> None:
    '''Checks for exit code 1 by running an existing code.'''
    exit_code = pytest_runner('1', get_code=True)   # This test gives exit 1.
    assert exit_code == 1

def test_exit_2() -> None:
    '''Checks for exit code 2 by running an existing code.'''
    exit_code = pytest_runner('3', get_code=True)   # This test gives exit 2.
    assert exit_code == 2


# This exit code was relegated and will be removed soon.
# See docs/IceBrakes API.txt for me info on exit code 3.
def _test_exit_3() -> None:
    '''Checks for exit code 3 by running an existing code.'''
    exit_code = pytest_runner('4', get_code=True)   # This test gives exit 3.
    assert exit_code == 2

#Copyright © 2023 Lars S.