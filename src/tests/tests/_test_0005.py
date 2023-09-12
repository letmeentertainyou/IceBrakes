'''Another test where the feature is yet to be implemented.
This time check for #$ in for loops.
'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
for i in range(55):
    BAR = i    #$
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('5')


#Copyright © 2023 Lars S.
