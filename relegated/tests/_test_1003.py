"""This test lints the entire testing dir and sends it to a single file."""
from os.path import isfile
from os import system

from src.tests.tools import TESTS, MAIN, DATA, filecmp


def test() -> None:
    """
    This test as flawed from the ground up, and constantly requires generating new data.
    It is relegated for those reasons. I should write another test for multi dir support.
    """

    name: str = "test_1003.txt"
    # Uncomment this line to generate new test data *this is needed often)
    # system(f'{MAIN} {TESTS} > {DATA}/perm/{name}')
    system(f"{MAIN} {TESTS} > {DATA}/tmp/{name}")
    assert isfile(f"{DATA}/perm/{name}")
    assert isfile(f"{DATA}/tmp/{name}")
    assert filecmp(f"{DATA}/perm/{name}", f"{DATA}/tmp/{name}")


# Copyright © 2023 Lars S.
