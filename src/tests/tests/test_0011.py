'''This test insures that +=, and *=, etc are ignored by
#$ checks but are still checked against for reassignment.
The line BAR*= 0 will be ignored because you cannot mutate
a variable and declare it immutable in one go. That's bad usage baby!'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
BAR = 0 #$
BAR*= 0 #$
BAR-= 0
BAR/= 100
BAR//= 1000
BAR%= 549534953
BAR = 'fleventyfour'
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('11')


#Copyright © 2023 Lars S.
