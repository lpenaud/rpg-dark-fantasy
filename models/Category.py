#!/usr/bin/env python
# coding: utf-8

from config import Sqlite, utils

class Category(Sqlite.Model):
    """docstring for Category."""
    def __init__(self, db):
        super(Category, self).__init__("Category", db)
        self.id = Sqlite.Field(
            name = "id",
            type = "INTEGER",
            primary = True,
            autoincrement = True,
            unique = True
        )
        self.name = Sqlite.Field(
            name = "name",
            type = "TEXT"
        )
        self.db.createTable(self)
