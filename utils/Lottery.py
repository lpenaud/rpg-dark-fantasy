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
        self.__items = {
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

        for item in self.__items.values():
            for i in range(0, len(item['items'])):
                for key,value in item['items'][i].items():
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

                item['items'][i]['categorie'] = tmpCat
                tmpStr = ""

        self.__history = []
        self.__minRarity = 1000 # Commun
        self.__maxRarity = 1 # Mythical

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
                'item': self.__items[value[0]]['items'][value[1]],
                'options': self.__items[value[0]]['options']
            })

        return tuple(history)

    @property
    def items(self):
        """
        Getter of items

        :return: A copy of item of Lottery
        :rtype: list
        """
        return self.__items.copy()

    @property
    def minRarity(self):
        """
        Getter of minRarity

        :return: The minimum rarity
        :rtype: int
        """
        return self.__minRarity

    @minRarity.setter
    def minRarity(self, val):
        """
        Setter of minRarity

        :param val: The new value of the minimum rarity
        :type val: int or str
        :raises TypeError: if val param type is not a str or int
        :raises ValueError: if the new value is less than the maximum rarity
        """
        if isinstance(val, int):
            tmp = val
        elif isinstance(val, str):
            tmp = self.deterTupleRarity(val)[1]
        else:
            raise TypeError("minRarity has to be a <str> or a <int>")
        if tmp < self.__maxRarity:
            raise ValueError("minRarity has to be higher than maxRarity")
        self.__minRarity = tmp

    @property
    def maxRarity(self):
        """
        Getter of maxRarity

        :return: The maximun rarity
        :rtype: int
        """
        return self.__maxRarity

    @maxRarity.setter
    def maxRarity(self, val):
        """
        Setter of maxRarity

        :param val: The new value of the maximun rarity
        :type val: int or str
        :raises TypeError: if val param type is not a str or int
        :raises ValueError: if the new value is higher than the minimum rarity
        """
        if isinstance(val, int):
            tmp = val
        elif isinstance(val, str):
            tmp = self.deterTupleRarity(val)[0]
        else:
            raise TypeError("maxRarity has to be a <str> or a <int>")
        if tmp > self.__minRarity:
            raise ValueError("maxRarity has to be less than minRarity")
        self.__maxRarity = tmp

    def deterNameRarity(self, number):
        """
        Method which determine the rarity string from a number

        :param number: Number which represent a rarity value
        :type number: int
        :return: String which represent a rarity value or nothing if number don't correspond at any rarity
        :rtype: str or None
        """
        for key, obj in self.__items.items():
            if number in key:
                return obj['options']['rarity']
        return None

    def deterTupleRarity(self, nameRarity):
        """
        Method which determine the minimum and the maximun number of a rarity

        :param nameRarity: Name of a rarity
        :type nameRarity: str
        :return: A tuple with the minimum and maximun number of a rarity
        :rtype: tuple
        :raise NameError: If the nameRarity param don't correspond at any rarity
        """
        for key, obj in self.__items.items():
            if nameRarity == obj['options']['rarity']:
                return key
        raise NameError(val + " - rarity unknown")

    def loot(self, keepHistory=False):
        """
        Play the Lottery

        :param keepHistory: If the loot is keep in history of Lottery by default False
        :type keepHistory: bool
        :return: A item with its options (dict with color and rarity)
        :rtype: dict
        """
        randNum = rand.randint(self.__maxRarity, self.__minRarity)
        category = {}
        indexItem = 0

        for key in self.__items.keys():
            if randNum >= key[0] and randNum <= key[1]:
                category = self.__items[key]
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
        :return: Text to display with print function or in label
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
