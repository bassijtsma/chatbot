from pymongo import MongoClient

class Chatrules:

    client = MongoClient()
    db = client.chatbot

    def __init__(self, database):
        Chatrules.db = client.database

    def findRules(self):
        cursor =  db.chatrules.find()
        for document in cursor:
            print(document)
