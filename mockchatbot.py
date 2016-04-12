'''
Mockchatbot with keyboard input instead of whatsapp chat chatinput.

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

'''
from database.sampledata                               import Sampledata
from database.db                                       import Db
from datetime                                          import time, tzinfo, datetime, timedelta
import datetime as dt
import time
import re
import logging, sys


logging.basicConfig(stream=sys.stderr, level=logging.INFO)
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
db = Db()
sb = Sampledata()
messages = db.getMessages()
conversations = sb.getConversations()
resetmsg = 'chatreset'
conversationTimeoutThreshold = dt.timedelta(seconds=10)

# Keeps track of the state of different conversations, so different people
# can talk to the bot at the same time without the chat intermingling a
# response.MessageProtocolEntity.getFrom() will be key.The most recent
# interaction with the bot will be tracked to figure out if the conversation
# has timed out and should be reset. Finally, it tracks how far into the
# conversation they are.
# conversationstates = {
#     m.getFrom() : [
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr}],
#     m.getFrom() : [
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr}],
#     m.getFrom() : [
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
#         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr}]
# }
#
# messages: [
#   { "m_nr" : 1, "qtext" : "hoi1", "rtext" : "doei 1", "is_alternative" : False, "conv_id" : 1 },
#        ..]

conversationstates = {}


def askForInput():
    input = raw_input("Your chat message:\n")
    return input.lower()


# searces through self.messages to find if the incoming message
# matches any of the preprogramming input
def findMessageQuestionMatches(incomingmessage):
    matches = []
    for message in messages:
        if (re.search(r'\b' + message['qtext'] + r'\b', incomingmessage)):
            matches.append(message)
    return matches


def isFirstQuestion(question):
    return (question['m_nr'] == 1)


def isUserRegisteredInConversationState(messageSender):
    return (messageSender in conversationstates)


def isFollowUpQuestion(messageSender, question):
    m_nrs = getm_nrsListForConvId(question['conv_id'])
    print m_nrs
    try:
        for convstate in conversationstates[messageSender]:
            if convstate['conv_id'] == question['conv_id']:
                return question['m_nr'] == (convstate['mostrecentquestion'] + 1)
    except Exception, e:
        return False
    return False


def getm_nrsListForConvId(conv_id):
    m_nrs = []
    for msg in messages:
        if conv_id == msg['conv_id']:
            m_nrs.append(msg['m_nr'])
    return m_nrs


def hasConversationTimedOut(messageSender, question):
    try:
        for convstate in conversationstates[messageSender]:
            if convstate['conv_id'] == question['conv_id']:
                currenttime = datetime.utcnow()
                return (currenttime - convstate['mostrecentinteraction']) > conversationTimeoutThreshold
    except Exception, e:
        return False
    return False


# Logic of doom to check if a question requires a response
def shouldGetResponse(isFirstQuestion, isUserRegisteredInConversationState, isFollowUpQuestion, hasConversationTimedOut):
    logging.info([isFirstQuestion, isUserRegisteredInConversationState, isFollowUpQuestion, hasConversationTimedOut])
    if isFirstQuestion:
        if isUserRegisteredInConversationState:
            if hasConversationTimedOut:
                return True
            else:
                return False # TODO hmm, ask for a reset?
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


def updateConversationState(messageSender, question):
    if messageSender in conversationstates:
        for conversationstate in conversationstates[messageSender]:
            if conversationstate['conv_id'] == question['conv_id']:
                conversationstate['mostrecentinteraction'] = datetime.utcnow()
                conversationstate['mostrecentquestion'] = question['m_nr']
                return True
        # The conversation_id conv_id had no record in the conv state yet, add it
        conversationstates[messageSender].append({'conv_id' : question['conv_id'],
        'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['m_nr']})
        return True
    # First registration of record for messageSender
    else:
        conversationstates[messageSender] = [{'conv_id' : question['conv_id'],
        'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['m_nr']}]
        return True


def resetSendersConversationState(messageSender):
    try:
        return(conversationstates.pop(messageSender, True))
    except Exception, e:
        logging.info('User did not have conversationstate to reset')
        return False


def reinitialize(self):
    logging.info('Resetting. Fetching questions and responses from DB...')
    messages = db.getMessages()


# Functions entry point for layer clas. Side effect to getting responses:
# has to maintain a state of the current conversation
def getResponsesForMessage(inputText):
    returnResponses = []
    messageSender = 123
    try:
        message = inputText
    except Exception, e:
        logging.info(['Fail getBody, probably different msg Type (e.g. media). Error: ', e])
        return returnResponses

    if message == resetmsg:
        reinitialize()

    questionmatches = findMessageQuestionMatches(message)
    if questionmatches:
        for question in questionmatches:
            shouldGetResponseBool = shouldGetResponse(
            isFirstQuestion(question),
            isUserRegisteredInConversationState(messageSender),
            isFollowUpQuestion(messageSender, question),
            hasConversationTimedOut(messageSender, question)
            )
            if shouldGetResponseBool:
                response = question['rtext']
                isConvStateUpdated = updateConversationState(messageSender, question)
                print 'response: ', response, '\n conv state updated: ', isConvStateUpdated, '\n'
                returnResponses.append({'responseText' : response})
    return returnResponses

db.resetDBToTestState()
while True:
    inputText = askForInput()
    returnResponses = getResponsesForMessage(inputText)
    for returnResponse in returnResponses:
        print returnResponse
