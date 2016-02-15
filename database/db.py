from pymongo import MongoClient

'''
responsible for getting the questions and responses from DB
a question is: { id: int, text: string, conv_id: int}
a response is : { id: int, text: string, conv_id: int, response_to: [{id: int}, {id: int} ]}
'''


class Db:

    print 'importing DB'
    client = MongoClient()
    db = client.chatbot

    def __init__(self, database):
        Chatrules.db = client.database

    def getQuestions(self):
        cursor =  db.questions.find()
        for document in cursor:
            print document

    def getResponses(self):
        cursor = db.responses.find()
        for document in cursor:
            print document
