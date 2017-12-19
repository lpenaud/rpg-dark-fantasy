#!/usr/bin/env python3
# coding: utf-8

from config import Sqlite, Category

db = Sqlite.Database('../data/data.db')
cat = Category.Category(db)
print(cat.getNameFields())

db.dropTable(cat.tableName)
db.close()
