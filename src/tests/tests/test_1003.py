'''This is the same as test 0 but with an invalid filename. To test
the invalid file name case.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
# this doesn't matter because the test is given
# an incorrect file name on purpose so these lines
# will never be linted.
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('####')


#Copyright © 2023 Lars S.
