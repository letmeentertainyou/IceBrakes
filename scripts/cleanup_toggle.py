#!/bin/python3
"""This script toggles test_9999_cleanup.py on and off which helps because
while I don't want to push the tmp test data to the repo I often do need
to read that data to diagnose failing tests. I often manually disable and
reenable the cleanup test and this seeks to speed things up."""

from os import listdir, rename
from pathlib import PosixPath
from sys import argv


def toggle(unity: bool = False) -> None:
    """This is a real simpler toggle switch but when unity is True
    then the test can only be enabled and not disabled. We use this in unifier."""
    path: PosixPath = PosixPath(__file__).joinpath("../../src/tests/tests").resolve()

    enable = "test_9999_cleanup.py"
    disable = "_test_9999_cleanup.py"
    dir = listdir(path)

    if enable in dir and not unity:
        rename(f"{path}/{enable}", f"{path}/{disable}")
        print("the cleanup test is disabled.")

    elif disable in dir:
        rename(f"{path}/{disable}", f"{path}/{enable}")
        print("the cleanup test is enabled.")


if __name__ == "__main__":
    if "-en" in argv:
        toggle(unity=True)
    else:
        toggle()
