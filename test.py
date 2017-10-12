import os
import sys

curdir = os.path.abspath(os.curdir)
sys.path.insert(0, curdir + '/utils')

from Lotery import *

example = Lotery('data/stuff.json')

# Type your test code here


