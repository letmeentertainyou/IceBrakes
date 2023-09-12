'''This test declares immutable vars on lines 12 and 13, but the 
declaration on line 13 is illegal because that var was mutable 
earlier in the file. This test demonstates what happens if you
modify a var before making it immutable.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
FOO = 'bar'
GOO = 'soap'
GOOFOO = f'{GOO}{FOO}'  #$
FOO = GOOFOO            #$
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation.'''
    pytest_runner('2')


#Copyright © 2023 Lars S.
