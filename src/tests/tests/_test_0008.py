'''Right now this project allows for you to modifiy lists, dicts, sets, 
and even tuples by assigning to their indivual values. This should be
pretty simple to implement.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
BAR = [0, 1, 2] #$
BAR[0] = 5555
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('8')


#Copyright © 2023 Lars S.
