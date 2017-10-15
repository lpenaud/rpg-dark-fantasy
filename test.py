import os
import sys

sys.path.insert(0, os.path.abspath(os.curdir) + '/utils')

from Lottery import *

example = Lottery('data/stuff.json')

def displayLoot(loot):
    for key, value in loot.items():
        print(key.title() + ':', sep=' ', end='\n')
        for subKey, subValue in value.items():
            print('   ', subKey + ':', subValue, sep=' ', end='\n')

# Type your test code here

randLoot = example.loot()
i = 1

while randLoot['options']['rarety'] != 'mythical':
    randLoot = example.loot()
    i += 1

displayLoot(randLoot)
print(i)
