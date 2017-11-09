#!/usr/bin/env/python3
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

# Type your test code here
randLoot = example.loot()
i = 1
listRarity = []
setRarity = 5

for obj in example.rarity.values():
    listRarity.append(obj['options']['rarity'])

choix = ''

while choix != 'e':
    choix = input('Faites un choix : J = Jouer // N = NombreEssais // R = ChangerRareté (default = mythical) // E = exit : ')

    if choix == 'J' or choix == 'j':    
        displayLoot(example.loot())

    if choix == 'N' or choix == 'n':
        randLoot = example.loot()
        i = 1
        while randLoot['options']['rarity'] != listRarity[setRarity]:
            randLoot = example.loot()
            i += 1

    if randLoot['options']['rarity'] == listRarity[setRarity]:
        print('Nombre d\'essais pour la rareté',listRarity[setRarity],':', i)
       
    if choix == 'R' or choix == 'r':
        while 1:
            for value in range(0,len(listRarity)):
                print(value, listRarity[value])
            setRarity = int(input('Entrez l\'index de nouvelle rareté cible : '))
            print('Rareté',listRarity[setRarity],'validée avec succès !')
            
            if setRarity < 0 and setRarity >= len(listRarity):
                print('Veuillez entrer une raretée valide : ')
                continue
            else:
                break
            
    if choix == 'E' or choix == 'e':
        print('Fin du programme')
        exit()