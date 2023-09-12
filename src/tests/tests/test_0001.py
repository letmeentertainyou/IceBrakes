'''This test declares immutable vars on lines 8 and 9, and modfies them on lines 13, and 14.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
BAR = 45           #$
CAR: int = 45      #$
FOO = 'str'

if __name__ == '__main__':
    BAR = 'mut'
    CAR = 45
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation.'''
    pytest_runner('1')


#Copyright © 2023 Lars S.
