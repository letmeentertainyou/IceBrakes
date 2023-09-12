'''Time to tests a class! We're setting an instance variable BAR to immutable,
that means no other class method, or property can modify self.BAR. This project needs
support for scopes and the 'self.' naming convention for this test to pass.'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
class Foo():
    '''This class has a few types of illegal assigment.'''
    def __init__(self, bar):
        self.bar = bar #$

    def modulate(self):
        '''Rule breaker!'''
        self.bar = 00 ** 0//10

    @property
    def goo(self):
        '''Properties need doc strings in mypy.'''
        self.bar = 0 ** 0 ** 0 ** 0
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('10')


#Copyright © 2023 Lars S.
