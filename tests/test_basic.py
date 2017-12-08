#!/usr/bin/env python3
# coding: utf-8

from config import Lottery

example = Lottery.Lottery('data/stuff.json')

# Type your test code here

print('test', example.deterTupleRarity('mythical'))
# example.minRarity = 'mythical'
# example.maxRarity = 'mythical'

print(str(example.maxRarity) + ' - ' + str(example.minRarity))
loot = example.loot(keepHistory=False)
print(
    loot['item']['nom'] + ' - ' + loot['options']['rarity'],
    sep='\n'
)
