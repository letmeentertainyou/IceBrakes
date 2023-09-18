'''This test is for hashmark comments, we expect a no linting declared message.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
#FOO = 0
#BAR = 0 #$
#GOO = 0
#CAR = 0 #$
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('13')


#Copyright © 2023 Lars S.
