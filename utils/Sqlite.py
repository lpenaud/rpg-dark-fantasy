#!/usr/bin/env python
# coding: utf-8

import sqlite3
import utils

class Database(sqlite3.Connection):
    """docstring for Database."""
    def __init__(self, db):
        super(Database, self).__init__(db)

    def createTable(self, model):
        req = "CREATE TABLE IF NOT EXISTS {}".format(str(model))
        print(req)
        self.cursor().execute(req)
        self.commit()

    def dropTable(self, table):
        self.cursor().execute("DROP TABLE {}".format(table))
        self.commit()

class Field(object):
    """docstring for Field."""
    def __init__(self, **args):
        argsKeys = args.keys()
        if not('name' in argsKeys):
            raise KeyError("Field must have a name")
        if not('type' in argsKeys):
            raise KeyError("Field must have a type")

        self.name = args['name']
        self.type = args['type'].upper()
        self.primary = args['primary'] if 'primary' in argsKeys else False
        self.autoincrement = args['autoincrement'] if 'autoincrement' in argsKeys else False
        self.unique = args['unique'] if 'unique' in argsKeys else False

    def __str__(self):
        return "{name} {sqlType} {primary} {autoincrement} {unique}".format(
            name = self.name,
            sqlType = self.type,
            primary = "PRIMARY KEY" if self.primary else "",
            autoincrement = "AUTOINCREMENT" if self.autoincrement else "",
            unique = "UNIQUE" if self.unique else ""
        ).strip()

class Model(object):
    """docstring for Categorie."""
    def __init__(self, name, db):
        self.tableName = name
        self.db = db

    def __str__(self):
        tmp = []
        for key in sorted(self.__dict__.keys()):
            if key == "tableName" or key == "db":
                continue
            else:
                tmp.append(str(self.__dict__[key]))
        return "{name}(\n    {fields}\n)".format(
            name = self.tableName,
            fields = ",\n    ".join(tmp)
        ).strip()

    def getNameFields(self):
        toReturn = []
        for key in sorted(self.__dict__.keys()):
            if key == "tableName" or key == "db":
                continue
            else:
                toReturn.append(key)
        return tuple(toReturn)
