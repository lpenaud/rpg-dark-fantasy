#!/usr/bin/env python3
# coding: utf-8

import os
import sys

sys.path.insert(0, os.path.abspath(os.curdir) + '/utils')

from Lottery import *

example = Lottery('data/stuff.json')

def displayLoot(loot):
    for key, value in loot.items():
        print(key.title() + ':', sep=' ', end='\n')
        for subKey, subValue in value.items():
            print('   ', subKey + ':', subValue, sep=' ', end='\n')

def clear():
    if os.name == 'posix':
        os.system("clear")
    else:
        os.system("cls")

randLoot = example.loot()
i = 1
listRarity = []
setRarity = 5

for key in sorted(example.rarity.keys(), reverse=True):
    listRarity.append(example.rarity[key]['options']['rarity'])

choix = ''

while 1:
    clear()
    print("J = Jouer",
        "N = Nombre d'essais",
        "R = Changer rareté (" + listRarity[setRarity] + ")",
        "Q = Quitter", sep='\n', end='\n')
    choix = input("Faites un choix : ").upper()

    clear()
    if choix == 'J':
        displayLoot(example.loot())

    elif choix == 'N':
        randLoot = example.loot()
        i = 1
        while randLoot['options']['rarity'] != listRarity[setRarity]:
            randLoot = example.loot()
            i += 1
        print("Nombre d'essais pour la rareté",listRarity[setRarity],':', i)

    elif choix == 'R':
        while 1:
            for value in range(0,len(listRarity)):
                print(value, listRarity[value])
            try:
                setRarity = int(input('Entrez l\'index de nouvelle rareté cible : '))
            except ValueError:
                print("Veuillez saisir un nombre")
                continue

            print('Rareté',listRarity[setRarity],'validée avec succès !')

            if setRarity < 0 and setRarity >= len(listRarity):
                print('Veuillez entrer une raretée valide : ')
                continue
            else:
                break

    elif choix == 'Q':
        break

    input("Appuyer sur <Enter> pour continuer.")

print('Fin du programme')
