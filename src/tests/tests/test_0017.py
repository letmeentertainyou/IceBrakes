# pylint: skip-file
'''This test is for the parenthesis skipper, none of these equal signs
mean assignment.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
FOO = lambda x: False
FOO(x='bar')      #$
def bar(name='', time=0.0, map=False):...
bar(name='name', time=0.1, map=True)    #$
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('17')


#Copyright © 2023 Lars S.
