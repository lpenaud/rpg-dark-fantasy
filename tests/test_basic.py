#!/usr/bin/env python3
# coding: utf-8

from config import Lottery

example = Lottery.Lottery('../data/stuff.json')

# Type your test code here

randLoot = example.loot()
i = 1

while randLoot['options']['rarety'] != 'legendary':
    randLoot = example.loot(True)
    i += 1

# displayLoot(randLoot)

for loot in example.history:
    print(example.displayLoot(loot))
