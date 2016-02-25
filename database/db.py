from pymongo import MongoClient
from sampledata import Sampledata


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
    sampledata = Sampledata()

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

    def _clearQuestions(self):
        cursor = db.questions.drop()
        return True

    def _clearResponses(self):
        cursor = db.responses.drop()
        return True

    def _clearConvIds(self):
        cursor = db.convs.drop()
        return True

    def _clearDb(self):
        try:
            self._clearQuestions()
            self._clearResponses()
            self._clearConvIds()
            return True
        except Exception, e:
            print e
            return False

    def insertTestData(self):
        testquestions = self.sampledata.getQuestions()
        testresponses = self.sampledata.getResponses()
        testconvs = self.sampledata.getConversations()
        db.questions.insert(testquestions)
        db.responses.insert(testquestions)
        db.conversations.insert(testconvs)

    def resetDBToTestState(self):
        _clearDb()
        insertTestData()


#
