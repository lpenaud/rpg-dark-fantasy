#!/usr/bin/env/python3
# coding: utf-8

from config import Lottery, Window

builder = Window.LotteryWindow()
window = builder.getWindow()
builder.changeImage("image-give-me-your-money", '../images/piece.png')
builder.changeTextLabel("label-give-me-your-money", "Hi stranger!")

Window.load(window, title="Loterie")