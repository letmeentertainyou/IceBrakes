# pylint: skip-file
'''This test is for multiline comments. We should get errors on lines 10 and 16g .'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
'''         #$
'''   """   #$
""" ''' ''' #$    
'''
#$
'''
#$ """ """
''' """ ''' """ ''' """ ''' #$
''' """ """ ''' """ """ ''' #$
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('18')


#Copyright © 2023 Lars S.
