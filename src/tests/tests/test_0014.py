# pylint: skip-file
'''Do scopes even work? Let's find out. If this test passes
our assignment on line 14 is legal and line 18 is illegal.

pylint is clever and also dislikes the code below. So now pylint
is disabled for this entire test.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
car = 33   #$

def bar(): #$
    '''Doc string for empty class.'''
    car = 45

class bar():
    '''Doc string for empty class.'''
    pass
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('14')


#Copyright © 2023 Lars S.
