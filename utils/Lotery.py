import random as rand
from dataJson import *

class Lotery(object):
    def __init__(self, strf):
        data = load(strf)
        self.__rarity = {
            'common': {
                'items':data['common'],
                'options': {
                    'rarety': (215, 1000),
                    'color':'grey'
                }
            }
            'unCommon': {
                'items':data['unCommon'],
                'options': {
                    'rarety': (65, 214),
                    'color':'green'
                }
            }
            'rare': {
                'items':data['rare'],
                'options': {
                    'rarety': (15, 64),
                    'color':'blue'
                }
            }
            'epic': {
                'items':data['epic'],
                'options': {
                    'rarety': (5, 14),
                    'color':'orange'
                }
            }
            'legendary': {
                'items':data['legendary'],
                'options': {
                    'rarety': (2, 4),
                    'color':'red'
                }
            }
            'mythical': {
                'items':data['mythical'],
                'options': {
                    'rarety': (1, 1),
                    'color':'purple'
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

        for key, value in self.rarity.items():
            if randNum >= value['options']['rarety'][0] and randNum <= value['options']['rarety'][1]:
                cat = self.rarity[key]
                break

        indexItem = rand.randint(0, len(cat))

        return {
            'item': cat['items'][indexItem],
            'options': cat['options']
        }
        

        
    


