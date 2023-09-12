'''A little spicy async recursion. I haven't made up my mind
about await and immutable variables yet. They are allowed in typescript
but js have promises so it's kind of one value cosplaying as another.
This test fails either way though because of recursive assignment.

Now I have no idea how I can possibly convincer a linter to look for that'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
async def foo():
    '''Lots of sings here.'''
    # pylint: disable-next=unused-variable
    bar = await foo()    #$
##################################################
################ END TEST CODE ###################
##################################################

def test() -> None:
    '''This is the default test implementation, call a test with the number of your test.'''
    pytest_runner('9')


#Copyright © 2023 Lars S.
