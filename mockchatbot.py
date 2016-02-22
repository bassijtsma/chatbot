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
conversationstate = {}

#TODO: ook bijhouden welk question ze zjin voor verschillende gesprek IDs
# Keeps track of the state of different conversations, so different people
# can talk to the bot at the same time without the chat intermingling a response
# messageProtocolEntity.getFrom() will be key.The most recent interaction with
# the bot will be tracked to figure out if the conversation has timed out and
# should be reset. Finally, it tracks how far into the conversation they are.
# conversationstate =
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




# conv_name = getConvName(conv_id)

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

# checks the conversationstate if prerequesite have been met to get a response
def shouldGetResponse(messageSender, questionmatches):
    for questionmatch in questionmatches:
        if messageSender in conversationstate:
            # Check the prerequesites
            for state in conversationstate[messageSender]:
                if questionmatch['conv_id'] == state['conv_id']:
                    print 'TODO'
        else:
            # if the 1st question, prerequesite is met. Add record to conversationstate
            if questionmatch['q_nr'] == 1:
                addInitialMessageSenderRecord(messageSender, questionmatch)
    print conversationstate


#TODO: LOGIC OF DOOM.
# refactor: function name implies boolean but has side effect of
# updating the conversationstate. Also logic is super difficult, try to split up
# misschien eerst test cases maken
def shouldGetResponse(messageSender, questionmatches):
    for question in questionmatches:
        if messageSender not in conversationstate:
            if isFirstQuestionInConversation(question):
                addInitialMessageSenderRecord(messageSender, question)
                return True
        else:
            convStateMatch = findConvStateMatch(messageSender, question)
            if isFirstQuestionInConversation(question):
                print 'hier'
                if convStateMatch:
                    if hasConversationTimedOut(convStateMatch):
                        #TODO: Add to conversationstate, return True
                        print 'has conv timed out en true!'
                        return True
                else:
                    #TODO: add to conversationstate, return True
                    'geen conv match en eerste vraag, en true!'
                    return True
            else:
                print ' daar'
                # if isQuestionFollowUp(question, convStateMatch):
                #     #TODO: ADd to conversation state, return True
                #     print 'true'
                #     return True


def updateConversationState(messageSender, question):
    for state in conversationstate[messageSender]:
        if question['conv_id'] == state['conv_id']:
            return True # TODO

def isFirstQuestionInConversation(question):
    return (question['q_nr'] == 1)


def isQuestionFollowUp(question, convStateMatch):
    if question['q_nr'] == (convStateMatch['mostrecentquestion'] + 1):
        return True
    return False


def findConvStateMatch(messageSender, question):
    for state in conversationstate[messageSender]:
        if question['conv_id'] == state['conv_id']:
            return state
    return False


def addInitialMessageSenderRecord(messageSender, question):
    conversationstate.setdefault(messageSender, [])
    stateitem = {}
    stateitem['conv_id'] = question['conv_id']
    stateitem['mostrecentinteraction'] = datetime.utcnow()
    stateitem['mostrecentquestion'] = 1
    conversationstate[messageSender].append(stateitem)


def hasConversationTimedOut(convStateMatch):
    currenttime = datetime.utcnow()
    return (currenttime - convStateMatch['mostrecentinteraction']) > conversationTimeoutThreshold


def updateConversationState(messageSender, question_nr):
    conversationstate[messageSender]['mostrecentinteraction'] = datetime.utcnow()
    conversationstate[messageSender]['question_nr'] = question_nr


def resetConversationStateForSender(messageSender):
    conversationstate[messageSender]['question_nr'] = 1
    conversationstate[messageSender]['mostrecentinteraction'] = datetime.utcnow()


messageSender = 123

while True:
    message = askForInput()
    questionmatches = findMessageQuestionMatches(messageSender, message)
    if questionmatches:
        shouldGetResponse(messageSender, questionmatches)

        # print conversationstate, '\n'

    else:
        # no match, just wait for next input. TODO: any handling needed?
        continue











#
