# pylint: skip-file
'''This test is for single line strings, none of these declarations are valid.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
'BAR = 0 '#$
"CAR = 0 "#$
'''BAR = 0 '''#$
"""CAR = 0 """#$
'def car(value=12, index=False)'#$
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('16')


#Copyright © 2023 Lars S.
