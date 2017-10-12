import random as rand
from utils.dataJson import *

class Lotery(object):
    def __init__(self, strf):
        data = load(strf)
        self._rarity = {
            (215, 1000): {
                'items':data['commun'],
                'options': {
                    'rarety':'commun',
                    'color':'gray'
                }
            }
        }
        self._history = []

    @property
    def rarity(self):
        return self._rarity

    @property
    def history(self):
        return self._history

    def loot(self):
        randNum = rand.randint(1, 1000)
        cat = ''

        for key, value in self._rarity.items():
            print(randNum)
            if randNum >= key[0] and randNum <= key[1]:
                cat = self._rarity[key]
                break

        indexItem = rand.randint(0, len(cat))

        return {
            'item': cat['items'][indexItem],
            'options': cat['options']
        }
        

        
    


