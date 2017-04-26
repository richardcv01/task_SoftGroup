from pymongo import MongoClient
import pymongo

class Mongo():
    def __init__(self, name_bd='test', name_col='mycoll'):
        self.name_bd = name_bd
        self.name_col = name_col
        self.connection = MongoClient()
        self.db = self.connection[self.name_bd]
        self.coll = self.db[self.name_col]
        self.coll.create_index('url', unique=True)

    def insert(self, title, url, author,text, price, currency):
        #if not self.coll.find_one({"url":url}):
        doc = {'title':title, 'url':url, 'author':author, 'text':text, 'price':price, 'currency':currency}
            #self.coll.insert(doc)
        try:
            self.coll.insert(doc)
        except pymongo.errors.DuplicateKeyError:
            pass


