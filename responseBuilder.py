from database.sampledata                               import Sampledata
from database.db                                       import Db
from datetime                                          import time, tzinfo, datetime, timedelta
import datetime as dt
import time
import re
import logging, sys

class ResponseBuilder:
    # logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    # logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    db = Db()
    messages = db.getMessages()
    conversations = db.getConversations()
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

    # searces through self.messages to find if the incoming message
    # matches any of the preprogramming input
    def findMessageQuestionMatches(self, incomingmessage):
        print
        matches = []
        for message in self.messages:
            loweredmessage = message['qtext'].lower()
            if (re.search(r'\b' + loweredmessage + r'\b', incomingmessage)):
                matches.append(message)
            elif loweredmessage == incomingmessage:
                matches.append(message)
        return matches


    def isFirstQuestion(self, question):
        return (question['m_nr'] == 1)


    def isUserRegisteredInConversationState(self, messageSender):
        return (messageSender in self.conversationstates)


    def isFollowUpQuestion(self, messageSender, question):
        m_nrs = self.getm_nrsListForConvId(question['conv_id'])
        try:
            for convstate in self.conversationstates[messageSender]:
                if convstate['conv_id'] == question['conv_id']:
                    return question['m_nr'] == (convstate['mostrecentquestion'] + 1)
        except Exception, e:
            return False
        return False



    # TODO: sort list based on m_nr and base decision on index rather than
    # m_nr. cannot guarantee the numebrs will be follow ups in frontend when
    # in situation: mnrs: 1, 2, 3, 4,  2 and 3 are set to alternative. thisll
    # become 1, 2, 2, 4. 4  is no longer follow up
    def getm_nrsListForConvId(self, conv_id):
        m_nrs = []
        for msg in self.messages:
            if conv_id == msg['conv_id']:
                m_nrs.append(msg['m_nr'])
        return m_nrs


    def hasConversationTimedOut(self, messageSender, question):
        try:
            for convstate in self.conversationstates[messageSender]:
                if convstate['conv_id'] == question['conv_id']:
                    currenttime = datetime.utcnow()
                    return (currenttime - convstate['mostrecentinteraction']) > self.conversationTimeoutThreshold
        except Exception, e:
            return False
        return False


    # Logic of doom to check if a question requires a response
    # probably better with switch statement
    def shouldGetResponse(self, isFirstQuestion, isUserRegisteredInConversationState, isFollowUpQuestion, hasConversationTimedOut):
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


    def updateConversationState(self, messageSender, question):
        if messageSender in self.conversationstates:
            for conversationstate in self.conversationstates[messageSender]:
                if conversationstate['conv_id'] == question['conv_id']:
                    conversationstate['mostrecentinteraction'] = datetime.utcnow()
                    conversationstate['mostrecentquestion'] = question['m_nr']
                    return True
            # The conversation_id conv_id had no record in the conv state yet, add it
            self.conversationstates[messageSender].append({'conv_id' : question['conv_id'],
            'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['m_nr']})
            return True
        # First registration of record for messageSender
        else:
            self.conversationstates[messageSender] = [{'conv_id' : question['conv_id'],
            'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['m_nr']}]
            return True


    def resetSendersConversationState(self, messageSender):
        try:
            return(self.conversationstates.pop(messageSender, True))
        except Exception, e:
            logging.info('User did not have conversationstate to reset')
            return False


    def reinitialize(self):
        logging.info('Resetting. Fetching questions and responses from DB...')
        self.messages = db.getMessages()


    # Function entry point for layer clas. Side effect for getting responses:
    # has to maintain a state of the current conversation. Probably not scaleable
    def getResponsesForMessage(self, messageProtocolEntity):
        returnResponses = []
        messageSender = messageProtocolEntity.getFrom()
        try:
            message = messageProtocolEntity.getBody().lower()
        except Exception, e:
            logging.info(['Fail getBody, probably different msg Type (e.g. media). Error: ', e])
            return returnResponses

        if message == self.resetmsg:
            self.reinitialize()



        questionmatches = self.findMessageQuestionMatches(message)
        print questionmatches
        if questionmatches:
            for question in questionmatches:
                shouldGetResponseBool = self.shouldGetResponse(
                self.isFirstQuestion(question),
                self.isUserRegisteredInConversationState(messageSender),
                self.isFollowUpQuestion(messageSender, question),
                self.hasConversationTimedOut(messageSender, question)
                )
                if shouldGetResponseBool:
                    response = question['rtext']
                    isConvStateUpdated = self.updateConversationState(messageSender, question)
                    print 'response: ', response, '\n conv state updated: ', isConvStateUpdated, '\n'
                    returnResponses.append({'responseText' : response})
        print self.conversationstates
        return returnResponses
