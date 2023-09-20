'''This is the same as test 0 but with an invalid filename. To test
the invalid file name case.'''

from os import system
from os.path import isfile

from src.tests.tools import TESTS, MAIN, DATA, filecmp

##################################################
############### BEGIN TEST CODE ##################
##################################################
# this doesn't matter because the test is given
# an incorrect file name on purpose so these lines
# will never be linted.
############################test_####.py######################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    name: str = 'test_####.txt'
    system(f'{MAIN} {TESTS}/test_####.py > {DATA}/tmp/{name}')
    assert isfile(f'{DATA}/perm/{name}')
    assert isfile(f'{DATA}/tmp/{name}')
    assert filecmp(f'{DATA}/perm/{name}', f'{DATA}/tmp/{name}')



#Copyright © 2023 Lars S.
