from database.sampledata import Sampledata
from database.db import Db
from datetime import time, tzinfo, datetime, timedelta
import datetime as dt
import time
import re


db = Db()
sampledata = Sampledata()
questions = sampledata.getQuestions()
responses = sampledata.getResponses()
conversations = sampledata.getConversations()
resetmsg = 'chatreset'
conversationTimeoutThreshold = dt.timedelta(minutes=4)

conversationstates = {}
# Keeps track of the state of different conversations, so different people
# can talk to the bot at the same time without the chat intermingling a response
# messageProtocolEntity.getFrom() will be key.The most recent interaction with
# the bot will be tracked to figure out if the conversation has timed out and
# should be reset. Finally, it tracks how far into the conversation they are.
# conversationstates =
# {
#     m.getFrom() : [
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr}],
#     m.getFrom() : [
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr}],
#     m.getFrom() : [
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr}]
# }

def askForInput():
    input = raw_input("Your chat message:\n")
    return input.lower()


def getConvName(conv_id):
    for conv in conversations:
        if conv_id == conv['conv_id']:
            print 'the conv name is:', conv['conv_name']
            return conv['conv_name']

def findMessageQuestionMatches(messageSender, message):
    matches = []
    for question in questions:
        if (re.search(r'\b' + question['text'] + r'\b', message)):
            matches.append(question)
    return matches


def isFirstQuestion(question):
    return (question['q_nr'] == 1)


def isFollowUpQuestion(messageSender, question):
    q_nrs = getq_nrsList(question['conv_id'])
    try:
        for convstate in conversationstates[messageSender]:
            if convstate['conv_id'] == question['conv_id']:
                return (q_nrs.index(convstate['mostrecentquestion']) + 1 == q_nrs.index(question['q_nr']))
    except Exception, e:
        return False
    return False


def getq_nrsList(conv_id):
    q_nrs = []
    for question in questions:
        if conv_id == question['conv_id']:
            q_nrs.append(question['q_nr'])
    return q_nrs

def hasConversationTimedOut(messageSender, question):
    try:
        for convstate in conversationstates[messageSender]:
            if convstate['conv_id'] == question['conv_id']:
                currenttime = datetime.utcnow()
                return (currenttime - convstate['mostrecentinteraction']) > conversationTimeoutThreshold
    except Exception, e:
        return False
    return False

def isUserRegisteredInConversationState(messageSender):
    return (messageSender in conversationstates)


def addInitialMessageSenderRecord(messageSender, question):
    conversationstates.setdefault(messageSender, [])
    stateitem = {}
    stateitem['conv_id'] = question['conv_id']
    stateitem['mostrecentinteraction'] = datetime.utcnow()
    stateitem['mostrecentquestion'] = question['q_nr']
    conversationstates[messageSender].append(stateitem)


# Logic of doom
def shouldGetResponse(isFirstQuestion, isUserRegisteredInConversationState, isFollowUpQuestion, hasConversationTimedOut):
    print isFirstQuestion, isUserRegisteredInConversationState, isFollowUpQuestion, hasConversationTimedOut
    if isFirstQuestion:
        if isUserRegisteredInConversationState:
            if hasConversationTimedOut:
                return True
            else:
                return False # TODO ASK FOR RESET?
        else:
            return True
    else:
        if isUserRegisteredInConversationState:
            if isFollowUpQuestion:
                return True
            else:
                return False
        else:
            return False


def findMatchingResponse(question):
    for response in responses:
        if question['conv_id'] == response['conv_id'] and question['q_nr'] == response['response_to_q']:
            return response


def updateConversationState(messageSender, question):
    if messageSender in conversationstates:
        for conversationstate in conversationstates[messageSender]:
            if conversationstate['conv_id'] == question['conv_id']:
                conversationstate['mostrecentinteraction'] = datetime.utcnow()
                conversationstate['mostrecentquestion'] = question['q_nr']
                return True
        # conv_id had no record in the conv state yet, add it
        conversationstates[messageSender].append({'conv_id' : question['conv_id'], 'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['q_nr']})
        return True
    # First registration of record for messageSender
    else:
        conversationstates[messageSender] = [{'conv_id' : question['conv_id'], 'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['q_nr']}]
        return True


def resetSendersConversationState(messageSender):
    try:
        return(conversationstates.pop(messageSender, True))
    except Exception, e:
        return False


messageSender = 123
# db.insertTestData()

# Simulate the chatloop
while True:

    # Simulate incoming messages
    message = askForInput()

    if message == resetmsg:
        if resetSendersConversationState(messageSender):
            print 'conversation state has been reset'

    questionmatches = findMessageQuestionMatches(messageSender, message)
    if questionmatches:
        for question in questionmatches:
            isFirstQuestionBool = isFirstQuestion(question)
            isFollowUpQuestionBool = isFollowUpQuestion(messageSender, question)
            isUserRegisteredInConversationStateBool = isUserRegisteredInConversationState(messageSender)
            hasConversationTimedOutBool = hasConversationTimedOut(messageSender, question)

            shouldReceiveResponse = shouldGetResponse(isFirstQuestionBool,
            isUserRegisteredInConversationStateBool, isFollowUpQuestionBool, hasConversationTimedOutBool)
            print 'should receive response?', shouldReceiveResponse
            if shouldReceiveResponse:
                response = findMatchingResponse(question)
                isConvStateUpdated = updateConversationState(messageSender, question)
                print response, '\n conv state updated: ',isConvStateUpdated, '\n'
    else:
        # no match, just wait for next input. TODO: any handling needed?
        continue


'''
SUPERNAIVE bruteforce solution for prototype implementation.
1. A message comes in
2. Go through all defined questions, and get all matches
3. For all matches, see if the prerequisites for them have been met:
    3a. its the first question in the conversation id, or
    3a. less than <conversationTimeoutThreshold> time ago, or
    3b. all questions that should have come before were already messaged
4. If the prerequisites have been met, go through all responses, and find the
 corresponding answer to the question
5. Echo the corresponding question
6. Update the conversationstate


Logictree for sending response shown below. TRUE should receive response,
FALSE should not, RESET should ask the user to reset (still TODO). 4 Booleans:
isFirstQuestion
isFollowUpQuestion
isUserRegisteredInConversationState
hasConversationTimedOut

isFirstQuestion:
    yes: isUserRegisteredInConversationState:
        no: TRUE
        yes: hasConversationTimedOut
            yes: TRUE
            no: RESET
    no: isUserRegisteredInConversationState:
        no: FALSE
        yes: isFollowUpQuestion:
            yes: TRUE
            no: FALSE
'''
