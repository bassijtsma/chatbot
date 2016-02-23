from database.sampledata import Sampledata
from datetime import time, tzinfo, datetime, timedelta
import datetime as dt
import time
import re

# Requirements:

# 1. User provides a message (question), bot responds
# 2a. User can ask a follow up question, and bot responds as a follow up
# 2b. The bot does not respond the follow up unless the first question has also been asked
# 3a. User can ask an alternative follow up question, providing several different answers
# 3b. Each alterantive question has its respective answer, even if the content of the answer is the same
# 4a. Defined messages (questions) should be transformed to lower case
# 4b. An input given by the user during the chat should be transformed to Lower case
# 5. All the words in the given input during the chat should be checked against the defined messages (questions)
# 6. Users can have multiple conversations with a chatbot at the same time

# Nice to Haves:
# 1. Discard determiners (lidwoorden)
# 2. Performing stemming on given input

conversationTimeoutThreshold = dt.timedelta(minutes=4)
sampledata = Sampledata()
questions = sampledata.getQuestions()
responses = sampledata.getResponses()
conversations = sampledata.getConversations()
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

# print questions
# print responses
# print conversations

def askForInput():
    input = raw_input("Your chat message:\n")
    return input.lower()


def getConvName(conv_id):
    for conv in conversations:
        if conv_id == conv['conv_id']:
            print 'the conv name is:', conv['conv_name']
            return conv['conv_name']


'''
SUPERNAIVE bruteforce solution:
1. A message comes in
2. Go through all defined questions, and get all matches
3. For all matches, see if the prerequisites for them have been met:
    3a. less than <conversationTimeoutThreshold> time ago
    3b. all earlier questions were already messaged, or
    3c. its the first message in the conversation id
4. If the prerequisites have been met, go through all responses, and find the
 corresponding answer to the question
5. Echo the corresponding question
6. Update the conversationstate
'''


def findMessageQuestionMatches(messageSender, message):
    matches = []
    for question in questions:
        if (re.search(r'\b' + question['text'] + r'\b', message)):
            matches.append(question)
    return matches


def updateConversationState(messageSender, question):
    for state in conversationstates[messageSender]:
        if question['conv_id'] == state['conv_id']:
            return True # TODO


def isFirstQuestion(question):
    return (question['q_nr'] == 1)


def isFollowUpQuestion(messageSender, question):
    try:
        for convstate in conversationstates[messageSender]:
            if convstate['conv_id'] == question['conv_id']:
                return (convstate['mostrecentquestion'] + 1) == question['q_nr']
    except Exception, e:
        return False
    return False


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

def updateConversationState(messageSender, question_nr):
    conversationstates[messageSender]['mostrecentinteraction'] = datetime.utcnow()
    conversationstates[messageSender]['question_nr'] = question_nr


def resetConversationStateForSender(messageSender):
    conversationstates[messageSender]['question_nr'] = 1
    conversationstates[messageSender]['mostrecentinteraction'] = datetime.utcnow()

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


messageSender = 123

while True:
    message = askForInput()
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
    else:
        # no match, just wait for next input. TODO: any handling needed?
        continue





# 2 possible ways to implement the logic. Return either TRUE or FALSE to
# update the users conversationstate, and go find a suitable response.
# isFirstQuestion
# isFollowUpQuestion
# isUserRegisteredInConversationState
# hasConversationTimedOut
#
# isFirstQuestion:
#     yes: isUserRegisteredInConversationState:
#         no: TRUE
#         yes: hasConversationTimedOut
#             yes: TRUE
#             no: RESET
#     no: isUserRegisteredInConversationState:
#         no: FALSE
#         yes: isFollowUpQuestion:
#             yes: TRUE
#             no: FALSE











#
