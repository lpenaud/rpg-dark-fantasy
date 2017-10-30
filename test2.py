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

SetRarety = 'mythical'
choix = ''

while choix != 'e':
    choix = input('Faites un choix : J = Jouer // N = NombreEssais // R = ChangerRareté (default = mythical) // E = exit : ')
    if choix == 'J' or choix == 'j':
        for loot in example.history:
            displayLoot(loot)
            break
    if choix == 'N' or choix == 'n':
        while randLoot['options']['rarety'] != SetRarety:
            randLoot = example.loot()
            i += 1

    if randLoot['options']['rarety'] == 'mythical':
        print('Nombre d\'essais pour la rareté :', i)
       
    if choix == 'R' or choix == 'r':
        SetRarety = input('Entrez la nouvelle rareté cible : ')
        if SetRarety == 'common' or SetRarety == 'unCommon' or SetRarety == 'rare' or SetRarety == 'epic' or SetRarety == 'legendary' or SetRarety == 'mythical':
            print('Rareté ',SetRarety,'validée')
            randLoot['options']['rarety'] = SetRarety
        else:
            print('Veuillez entrer une raretée valide : ')
            SetRarety = input('Entrez la nouvelle rareté cible : ')
            
    if choix == 'E' or choix == 'e':
        print('Fin du programme')
        exit()