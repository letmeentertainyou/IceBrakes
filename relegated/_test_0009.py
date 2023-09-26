'''This test has been relegated on account of it being utter nonsense. This test
will be deleted in the version after v0.1.8'''
from src.tests.tools import pytest_runner

##################################################
############### BEGIN TEST CODE ##################
##################################################
async def foo():
    # pylint: disable-next=unused-variable
    bar = await foo()    #$
##################################################
################ END TEST CODE ###################
##################################################

#Copyright © 2023 Lars S.
