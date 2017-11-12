#!/usr/bin/env python3
# coding: utf-8

from config import Lottery, Window

example = Lottery.Lottery('../data/stuff.json')

def button1_clicked(*args):
    randLoot = example.loot(keepHistory=False)
    i = 1

    while randLoot['options']['rarety'] != 'mythical':
        randLoot = example.loot(keepHistory=False)
        i += 1

    builder.displayLoot(2, randLoot)
    print(i)

builder = Window.LotteryWindow(example)
builder.changeImage("image-give-me-your-money", '../images/piece.png')
builder.changeTextLabel("label-give-me-your-money", "Hi stranger!")
Window.load(builder.getWindow(), title="Loterie")
