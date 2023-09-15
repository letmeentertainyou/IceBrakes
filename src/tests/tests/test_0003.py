'''This test has no #$ symbols and therefore won't be linted. We get a special
exit code 2 here.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
# WRITE TEST FOR INVALID FILE PATH (don't use an output file
# because there should be no input file for this test.)
FOO = {(k ** 2, v // 2) for k, v in enumerate(range(5000))}
GOO = (str(line) for line in FOO)
FOOGOO = dict(zip(FOO, GOO))
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation.'''
    pytest_runner('3')


#Copyright © 2023 Lars S.
