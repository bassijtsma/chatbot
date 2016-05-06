from responseBuilder import ResponseBuilder
from database.db import Db
from database.sampledata import Sampledata

db = Db()
rb = ResponseBuilder()
sampledata = Sampledata()

print 'starting...'

class SampleMessageProtocolEntity:
    def __init__(self, sender, message):
        self.sender = sender
        self.message = unicode(message)

    def getFrom(self):
        return self.sender

    def getBody(self):
        return self.message


db.clearTestIncomingMsg()
samplemessages = sampledata.getMessages()

testpass = 0
testfail = 0

for i, message in enumerate(samplemessages):
    print 'running test ', i, ' of: ', len(samplemessages)
    db.insertTestIncomingMsg({'message': message['qtext'], 'sender': 'testuser'})
    dbmessage = db.getMostRecentTestIncomingMsg()
    msgentity = SampleMessageProtocolEntity('testuser', dbmessage['message'])
    response = rb.getResponsesForMessage(msgentity)

    print response
    print '\n\n'
    print message

    try:
        if response[0]['rtext'] == message['rtext']:
            print 'test pass!'
            testpass =+ testpass
        else:
            print 'test fail:', response, message['rtext']
            testfail =+ testfail
    except Exception, e:
        testfail =+ testfail

print '\n\n\nnumber of tests passed: ', testpass, '\nnumber of test fail: ', testfail
