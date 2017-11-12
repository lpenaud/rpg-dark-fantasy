#!/usr/bin/env python3
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
                    'rarety': 'common',
                    'color': 'grey'
                }
            },
            (65, 214): {
                'items': data['unCommon'],
                'options': {
                    'rarety': 'unCommon',
                    'color': 'green'
                }
            },
            (15, 64): {
                'items': data['rare'],
                'options': {
                    'rarety': 'rare',
                    'color': 'blue'
                }
            },
            (5, 14): {
                'items': data['epic'],
                'options': {
                    'rarety': 'epic',
                    'color': 'orange'
                }
            },
            (2, 4): {
                'items': data['legendary'],
                'options': {
                    'rarety': 'legendary',
                    'color': 'red'
                }
            },
            (1, 1): {
                'items': data['mythical'],
                'options': {
                    'rarety': 'mythical',
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

        return history

    @property
    def rarity(self):
        return self.__rarity.copy()

    def loot(self, keepHistory=False):
        randNum = rand.randint(1, 1000)
        category = {}
        indexItem = 0

        for key in self.__rarity.keys():
            if randNum >= key[0] and randNum <= key[1]:
                category = self.__rarity[key]
                break

        indexItem = rand.randint(0, len(category['items']) - 1)

        if keepHistory:
            self.__history.append((key, indexItem))

        return {
            'item': category['items'][indexItem],
            'options': category['options']
        }

    def displayLoot(self, loot):
        txt = ""

        for key, value in loot.items():
            txt += key.title() + ':\n'
            for subKey, subValue in value.items():
                if subKey == 'color':
                    continue
                txt += '   ' + str(subKey) + ' : ' + str(subValue) + '\n'

        return txt
