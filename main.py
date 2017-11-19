#!/usr/bin/env python3
# coding: utf-8

import os
import sys

sys.path.insert(0, os.path.abspath(os.curdir) + '/utils')

from Lottery import Lottery
from Window import LotteryWindow
from utils import load, realPathDir

builder = LotteryWindow(Lottery(realPathDir()+'../data/stuff.json'))
