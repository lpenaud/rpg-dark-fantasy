import random as rand
from dataJson import *

class Lotery(object):
    def __init__(self, strf):
        data = load(strf)
        self.__rarity = {
            'commun': {
                'items':data['commun'],
                'options': {
                    'rarety': (215, 1000),
                    'color':'gray'
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
        randNum = rand.randint(215, 1000) # replace 215 by 0 when data is finish

        for key, value in self.rarity.items():
            if randNum >= value['options']['rarety'][0] and randNum <= value['options']['rarety'][1]:
                cat = self.rarity[key]
                break

        indexItem = rand.randint(0, len(cat))

        return {
            'item': cat['items'][indexItem],
            'options': cat['options']
        }
        

        
    


