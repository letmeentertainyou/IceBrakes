'''This test checks for in line assignment using the ugly :=
operator. This test isn't implemented yet because if isn't
being checked for as an assignment preface. 

I'm probably not going to implement this test, it's a very low priority
feature of the language to me.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
if (BAR:= 45) < 50:     #$
    print('Bad usage buddy.')
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('12')


#Copyright © 2023 Lars S.
