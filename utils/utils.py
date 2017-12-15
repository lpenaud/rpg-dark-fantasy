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

def isFrozen():
    """
    Test if the application is frozen (pyinstaller)

    :return: True/False depend if the application is frozen
    :rtype: bool
    """
    return getattr(sys, 'frozen', False)

def resolvePath(f):
    """
    Get absolute path of a file (All the files imports have to use this function)

    :param f: Paths relative to the file whose departure is the root of the application
    :type f: str
    :return: Absolute path of the file
    :rtype: str
    """
    if isFrozen():
        path = os.path.dirname(os.path.realpath(__file__)) + '/'
    else:
        path = os.path.dirname(os.path.realpath(__file__)) + '/../'

    return path + f
