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
questions = sb.getQuestions()
responses = sb.getResponses()
conversations = sb.getConversations()
resetmsg = 'chatreset'
conversationTimeoutThreshold = dt.timedelta(seconds=1)

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
conversationstates = {}




def askForInput():
    input = raw_input("Your chat message:\n")
    return input.lower()


def findMessageQuestionMatches(message):
    matches = []
    for question in questions:
        if (re.search(r'\b' + question['text'] + r'\b', message)):
            matches.append(question)
    return matches


def isFirstQuestion(question):
    return (question['q_nr'] == 1)


def isUserRegisteredInConversationState(messageSender):
    return (messageSender in conversationstates)


# Sorts all the questions and checks whether the index of the msg (within)
# the same conversation id) is a follow up of the most recent question
def isFollowUpQuestion(messageSender, question):
    q_nrs = getq_nrsListForConvId(question['conv_id'])
    try:
        for convstate in conversationstates[messageSender]:
            if convstate['conv_id'] == question['conv_id']:
                return (q_nrs.index(convstate['mostrecentquestion']) + 1 == q_nrs.index(question['q_nr']))
    except Exception, e:
        return False
    return False


def getq_nrsListForConvId(conv_id):
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


def getMatchingResponse(question):
    for response in responses:
        if question['conv_id'] == response['conv_id'] and question['_id'] == response['response_to_q_id']:
            return response


def updateConversationState(messageSender, question):
    if messageSender in conversationstates:
        for conversationstate in conversationstates[messageSender]:
            if conversationstate['conv_id'] == question['conv_id']:
                conversationstate['mostrecentinteraction'] = datetime.utcnow()
                conversationstate['mostrecentquestion'] = question['q_nr']
                return True
        # The conversation_id conv_id had no record in the conv state yet, add it
        conversationstates[messageSender].append({'conv_id' : question['conv_id'],
        'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['q_nr']})
        return True
    # First registration of record for messageSender
    else:
        conversationstates[messageSender] = [{'conv_id' : question['conv_id'],
        'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['q_nr']}]
        return True


def resetSendersConversationState(messageSender):
    try:
        return(conversationstates.pop(messageSender, True))
    except Exception, e:
        logging.info('User did not have conversationstate to reset')
        return False


def reinitialize(self):
    logging.info('Resetting. Fetching questions and responses from DB...')
    questions = db.getQuestions()
    responses = db.getResponses()
    resetSendersConversationState()


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
                response = getMatchingResponse(question)
                isConvStateUpdated = updateConversationState(messageSender, question)
                print 'response: ', response, '\n conv state updated: ', isConvStateUpdated, '\n'
                returnResponses.append({'responseText' : response['text']})
    return returnResponses


while True:
    inputText = askForInput()
    returnResponses = getResponsesForMessage(inputText)
    for returnResponse in returnResponses:
        print returnResponse
