#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import json

def load(strf):
    """
    load a JSON file in a dict

    :param strf: name of the json file
    :type strf: str
    :return: data in JSON file
    :rtype: dict
    """

    if not(isinstance(strf, str)):
        raise TypeError("arg must be a str")

    with open(strf, mode='r', encoding="utf-8") as f:
        tmp = json.loads(f.read())

    jsonData = {}

    for key, value in tmp.items(): #Enable set() class in list in JSON
        if isinstance(value, list) and "set" in value:
            obj = set(value)
            obj.remove("set")
        else:
            obj = value

        jsonData[key] = obj

    return jsonData

def realPathDir(f=__file__):
    """
    Get absolute path of a python script (useful when you have to import file)

    :return: Absolute path of python file
    :rtype: str
    """
    return os.path.dirname(os.path.realpath(f)) + '/'

def isFrozen():
    return getattr(sys, 'frozen', False)

def resolvePath(f):
    if isFrozen():
        path = realPathDir()
    else:
        path = realPathDir() + '../'

    return path + f
