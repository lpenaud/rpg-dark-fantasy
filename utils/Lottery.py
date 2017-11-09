#!/usr/bin/env/python3
# coding: utf-8

import random as rand
from dataJson import *

class Lottery(object):
    def __init__(self, strf):
        data = load(strf)
        self.__rarity = {
            (215, 1000): {
                'items': data['common'],
                'options': {
                    'rarity': 'common',
                    'color': 'grey'
                }
            },
            (65, 214): {
                'items': data['unCommon'],
                'options': {
                    'rarity': 'unCommon',
                    'color': 'green'
                }
            },
            (15, 64): {
                'items': data['rare'],
                'options': {
                    'rarity': 'rare',
                    'color': 'blue'
                }
            },
            (5, 14): {
                'items': data['epic'],
                'options': {
                    'rarity': 'epic',
                    'color': 'orange'
                }
            },
            (2, 4): {
                'items': data['legendary'],
                'options': {
                    'rarity': 'legendary',
                    'color': 'red'
                }
            },
            (1, 1): {
                'items': data['mythical'],
                'options': {
                    'rarity': 'mythical',
                    'color': 'purple'
                }
            }
        }
        self.__history = []

    @property
    def history(self):
        history = []

        for value in self.__history:
            history.append({
                'item': self.__rarity[value[0]]['items'][value[1]],
                'options': self.__rarity[value[0]]['options']
            })

        return tuple(history)

    @property
    def rarity(self):
        return self.__rarity.copy()

    def loot(self):
        randNum = rand.randint(1, 1000)
        category = {}
        indexItem = 0

        for key in self.rarity.keys():
            if randNum >= key[0] and randNum <= key[1]:
                category = self.rarity[key]
                break

        indexItem = rand.randint(0, len(category['items']) - 1)
        self.__history.append((key, indexItem))

        return {
            'item': category['items'][indexItem],
            'options': category['options']
        }
        

        
    


