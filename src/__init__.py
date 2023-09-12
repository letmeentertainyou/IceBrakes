#!/bin/python3
'''Because all the sub package __init__.pys look like this
   this file can be empty and work fine, as importing any other 
   module will fix the path, I'm leaving this here for legacy 
   reasons and to keep my projects formatted similarly'''

import os
import sys

sys.path.append(os.path.realpath(''))

#Copyright © 2023 Lars S.
