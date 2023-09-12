'''This test reveals a specific weakness of python which is that
most copies of things are shallow copies and simply refererence 
the original object. Now we can throw an error here but we have 
to parse to see if any other vars are being assigned the value of 
one of our immutable vars.

This would be a huge addiional piece of logic and linting. This test 
also brings to light the issues presented in test #8'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
BAR = [0, 1, 2] #$
FOO = BAR
FOO[0] = 2
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('7')


#Copyright © 2023 Lars S.
