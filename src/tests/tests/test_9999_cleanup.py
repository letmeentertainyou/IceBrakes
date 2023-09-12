'''Cleanup the src/tests/data/tmp dir.'''
from src.tests.tools import cleanup

##################################################
############### BEGIN TEST CODE ##################
##################################################
# Cleanup test has no code block, should always pass!
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''Calls the cleanup() function from tools.py after every other test runs.'''
    cleanup()


#Copyright © 2023 Lars S.
