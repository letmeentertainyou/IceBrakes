'''Defing a immmutable function inside a while loop. Illegal!s'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
while True:
    def bar(): #$
        '''You can't assign a var as immutable multiple times.'''
    break
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('6')


#Copyright © 2023 Lars S.
