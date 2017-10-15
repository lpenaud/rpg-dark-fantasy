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
        return self.__history.copy()

    @property
    def rarity(self):
        return self.__rarity.copy()

    def loot(self):
        randNum = rand.randint(1, 1000)
        category = {}
        indexItem = 0

        for key, value in self.rarity.items():
            if randNum >= key[0] and randNum <= key[1]:
                category = self.rarity[key]
                break

        indexItem = rand.randint(0, len(category['items']) - 1)

        return {
            'item': category['items'][indexItem],
            'options': category['options']
        }
        

        
    


