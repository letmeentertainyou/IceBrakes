# pylint: skip-file
'''This is another test for scopes but with a bit more complexity.
The illegal assignments are lines: 14, 23, 30
The legal assignments are lines: 11, 18, 19, 27, 34 '''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
def foo():                     # duplicate class
    class car():               #$
        pass

    class car():
        pass

def bar():                     # duplicate class functions
    class car():               #$
        def dar():             #$
            pass

        @property
        def dar():
            return None

def foobar():                  # overwritten class
    class car():               #$
        pass

    def car():
        pass

def barfoo():                  # no crimes here
    class car():               #$
        pass
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('15')


#Copyright © 2023 Lars S.
