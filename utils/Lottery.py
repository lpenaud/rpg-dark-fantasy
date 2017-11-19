#!/usr/bin/env python3
# coding: utf-8
import random as rand
from utils import *

class Lottery(object):
    """
    Create a Lottery with a json file

    :param strf: name of the json file which contain items
    :type strf: str
    """

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

        tmpCat = ""
        tmpStr = ""

        for rarity in self.__rarity.values():
            for i in range(0, len(rarity['items'])):
                for key,value in rarity['items'][i].items():
                    if key == "number" or key == "classe":
                        continue
                    tmpStr += value.lower() + " "

                if "parchemin" in tmpStr:
                    tmpCat = "parchment"

                elif "grimoire" in tmpStr:
                    tmpCat = "book"

                elif "bâton" in tmpStr:
                    tmpCat = "stick"

                elif "attaqu" in tmpStr or "arme" in tmpStr:
                    if "épée" in tmpStr:
                        tmpCat = "sword"
                    elif "hache" in tmpStr:
                        tmpCat = "axe"
                    else:
                        tmpCat = "att"

                elif "armure" in tmpStr or "casque" in tmpStr:
                    if "chaussure" in tmpStr or "botte" in tmpStr:
                        tmpCat = "shoe"
                    elif "casque" in tmpStr:
                        tmpCat = "helmet"
                    elif "bouclier" in tmpStr:
                        tmpCat = "shield"
                    else:
                        tmpCat = "armor"
                else:
                    tmpCat = "unknown"

                rarity['items'][i]['categorie'] = tmpCat
                tmpStr = ""


        self.__history = []

    @property
    def history(self):
        """
        Getter of history

        :return: History of Lottery with all loots (dict with item and options)
        :rtype: tuple
        """
        history = []

        for value in self.__history:
            history.append({
                'item': self.__rarity[value[0]]['items'][value[1]],
                'options': self.__rarity[value[0]]['options']
            })

        return tuple(history)

    @property
    def rarity(self):
        """
        Getter of rarity

        :return: A copy of rarity of Lottery
        :rtype: list
        """
        return self.__rarity.copy()

    def loot(self, keepHistory=False):
        """
        Play the Lottery

        :param keepHistory: If the loot is keep in history of Lottery by default False
        :type keepHistory: bool
        :return: A item with its options (dict with color and rarity)
        :rtype: dict
        """
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
        """
        Create a string with all informations of a loot

        :param loot: loot returned by Lottery.loot()
        :type loot: dict
        :return: Text to display with a print or in label
        :rtype: str
        """
        txt = ""

        for key, value in loot.items():
            txt += key.title() + ':\n'
            for subKey, subValue in value.items():
                if subKey == 'color':
                    continue
                txt += '   ' + str(subKey) + ' : ' + str(subValue) + '\n'

        return txt
