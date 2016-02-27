from database.sampledata                               import Sampledata
from database.db                                       import Db
from datetime                                          import time, tzinfo, datetime, timedelta
import datetime as dt
import time
import re


class IncomingMessageHandler:

    db = Db()
    questions = db.getQuestions()
    responses = db.getResponses()
    conversations = db.getConversations()
    resetmsg = 'chatreset'
    conversationTimeoutThreshold = dt.timedelta(seconds=1)

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
    conversationstates = {}


    def findMessageQuestionMatches(self, message):
        matches = []
        for question in self.questions:
            if (re.search(r'\b' + question['text'] + r'\b', message)):
                matches.append(question)
        return matches


    def isFirstQuestion(self, question):
        return (question['q_nr'] == 1)

    # Sorts all the questions and checks whether the index of the msg (within)
    # the same conversation id) is a follow up of the most recent question
    def isFollowUpQuestion(self, messageSender, question):
        q_nrs = self.getq_nrsListForConvId(question['conv_id'])
        try:
            for convstate in self.conversationstates[messageSender]:
                if convstate['conv_id'] == question['conv_id']:
                    return (q_nrs.index(convstate['mostrecentquestion']) + 1 == q_nrs.index(question['q_nr']))
        except Exception, e:
            return False
        return False


    def getq_nrsListForConvId(self, conv_id):
        q_nrs = []
        for question in self.questions:
            if conv_id == question['conv_id']:
                q_nrs.append(question['q_nr'])
        return q_nrs

    def hasConversationTimedOut(self, messageSender, question):
        try:
            for convstate in self.conversationstates[messageSender]:
                if convstate['conv_id'] == question['conv_id']:
                    currenttime = datetime.utcnow()
                    return (currenttime - convstate['mostrecentinteraction']) > self.conversationTimeoutThreshold
        except Exception, e:
            return False
        return False

    def isUserRegisteredInConversationState(self, messageSender):
        return (messageSender in self.conversationstates)


    def addInitialMessageSenderRecord(self, messageSender, question):
        self.conversationstates.setdefault(messageSender, [])
        stateitem = {}
        stateitem['conv_id'] = question['conv_id']
        stateitem['mostrecentinteraction'] = datetime.utcnow()
        stateitem['mostrecentquestion'] = question['q_nr']
        self.conversationstates[messageSender].append(stateitem)


    # Logic of doom
    def shouldGetResponse(self, isFirstQuestion, isUserRegisteredInConversationState, isFollowUpQuestion, hasConversationTimedOut):
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


    def getMatchingResponse(self,question):
        for response in self.responses:
            if question['conv_id'] == response['conv_id'] and question['q_nr'] == response['response_to_q']:
                return response


    def updateConversationState(self, messageSender, question):
        if messageSender in self.conversationstates:
            for conversationstate in self.conversationstates[messageSender]:
                if conversationstate['conv_id'] == question['conv_id']:
                    conversationstate['mostrecentinteraction'] = datetime.utcnow()
                    conversationstate['mostrecentquestion'] = question['q_nr']
                    return True
            # conv_id had no record in the conv state yet, add it
            self.conversationstates[messageSender].append({'conv_id' : question['conv_id'], 'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['q_nr']})
            return True
        # First registration of record for messageSender
        else:
            self.conversationstates[messageSender] = [{'conv_id' : question['conv_id'], 'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['q_nr']}]
            return True


    def resetSendersConversationState(self, messageSender):
        try:
            return(self.conversationstates.pop(messageSender, True))
        except Exception, e:
            return False


    #  TODO: also have to reset state, otherwise question_nrs dont align
    def reinitialize(self):
        print 'resetting questions and responses...'
        self.questions = db.getQuestions()
        self.responses = db.getResponses()


    def handleIncomingMessage(self, messageProtocolEntity):

        returnResponses = []
        messageSender = messageProtocolEntity.getFrom()

        try:
            message = messageProtocolEntity.getBody().lower()
        except Exception, e:
            print 'Fail getBody, probably different msg Type (e.g. media). Error: ', e
            return returnResponses

        if message == self.resetmsg:
            self.reinitialize()
            self.resetSendersConversationState()
            print 'conversation state has been reset'

        questionmatches = self.findMessageQuestionMatches(message)

        if questionmatches:
            for question in questionmatches:
                # could also remove Bool vars and simply call fn with fn calls as args. Dunno
                isFirstQuestionBool = self.isFirstQuestion(question)
                isUserRegisteredInConversationStateBool = self.isUserRegisteredInConversationState(messageSender)
                isFollowUpQuestionBool = self.isFollowUpQuestion(messageSender, question)
                hasConversationTimedOutBool = self.hasConversationTimedOut(messageSender, question)

                shouldGetResponseBool = self.shouldGetResponse(isFirstQuestionBool,
                isUserRegisteredInConversationStateBool, isFollowUpQuestionBool, hasConversationTimedOutBool)
                print 'should receive response?', shouldGetResponseBool
                if shouldGetResponseBool:
                    response = self.getMatchingResponse(question)
                    isConvStateUpdated = self.updateConversationState(messageSender, question)
                    print response, '\n conv state updated: ',isConvStateUpdated, '\n'

                    returnResponses.append({'responseText' : response['text']})

        return returnResponses
