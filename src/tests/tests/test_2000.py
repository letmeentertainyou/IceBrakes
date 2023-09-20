# pylint: skip-file
'''This test is for lines that only contain white space as that was causing a bug.
Now that whitespace is supported this test shouldn't cause a crash. If it ever does
then we know whitespace is to blame.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################

   
   

##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('2000')


#Copyright © 2023 Lars S.
