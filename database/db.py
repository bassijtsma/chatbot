from pymongo import MongoClient
'''
responsible for getting the questions and responses from DB
a question is: { id: int, text: string, conv_id: int}
a response is : { id: int, text: string, conv_id: int, response_to: [{id: int}, {id: int} ]}
'''

class Db:
    env = 'prod'
    client = MongoClient()
    questions = []
    responses = []

    def __init__(self):
        if self.env == 'prod':
            self.db = self.client.prod
        else:
            self.db = self.client.test

    def getQuestions(self):
        cursor =  db.questions.find().sort({'conv_id': 1, 'id' : 1})
        for document in cursor:
            self.questions.append(document)
            print 'nr of questions: ', len(self.questions)
        return self.questions

    def getResponses(self):
        cursor = db.responses.find().sort({'conv_id': 1, 'id' : 1})
        for document in cursor:
            self.responses.append(document)
            print 'nr of responses: ', len(self.responses)
            return self.responses
