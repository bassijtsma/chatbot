from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from database.sampledata                               import Sampledata
from database.db                                       import Db
from datetime                                          import time, tzinfo, datetime, timedelta
import datetime as dt
import time
import re

#TODO
# event listener die luisterd naar disconnect, en weer verbinding maakt
# org.openwhatsapp.yowsup.event.network.disconnected
# verify if reconnecting on discnonecting is feasible. something like: https://github.com/tgalal/yowsup/issues/921




class EchoLayer(YowInterfaceLayer):
    db = Db()
    questions = db.getQuestions()
    responses = db.getResponses()
    conversations = db.getConversations()
    resetmsg = 'chatreset'
    conversationTimeoutThreshold = dt.timedelta(seconds=5)

    conversationstates = {}

    def askForInput(self):
        input = raw_input("Your chat message:\n")
        return input.lower()


    def getConvName(self, conv_id):
        for conv in self.conversations:
            if conv_id == conv['conv_id']:
                print 'the conv name is:', conv['conv_name']
                return conv['conv_name']

    def findMessageQuestionMatches(self, messageSender, message):
        matches = []
        for question in self.questions:
            if (re.search(r'\b' + question['text'] + r'\b', message)):
                matches.append(question)
        return matches


    def isFirstQuestion(self, question):
        return (question['q_nr'] == 1)


    def isFollowUpQuestion(self, messageSender, question):
        q_nrs = getq_nrsList(question['conv_id'])
        try:
            for convstate in self.conversationstates[messageSender]:
                if convstate['conv_id'] == question['conv_id']:
                    return (q_nrs.index(convstate['mostrecentquestion']) + 1 == q_nrs.index(question['q_nr']))
        except Exception, e:
            return False
        return False


    def getq_nrsList(self, conv_id):
        q_nrs = []
        for question in self.questions:
            if conv_id == question['conv_id']:
                q_nrs.append(question['q_nr'])
        return q_nrs

    def hasConversationTimedOut(self, messageSender, question):
        try:
            for convstate in conversationstates[messageSender]:
                if convstate['conv_id'] == question['conv_id']:
                    currenttime = datetime.utcnow()
                    return (currenttime - convstate['mostrecentinteraction']) > conversationTimeoutThreshold
        except Exception, e:
            return False
        return False

    def isUserRegisteredInConversationState(self, messageSender):
        return (messageSender in conversationstates)


    def addInitialMessageSenderRecord(self, messageSender, question):
        conversationstates.setdefault(messageSender, [])
        stateitem = {}
        stateitem['conv_id'] = question['conv_id']
        stateitem['mostrecentinteraction'] = datetime.utcnow()
        stateitem['mostrecentquestion'] = question['q_nr']
        conversationstates[messageSender].append(stateitem)


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


    def findMatchingResponse(self,question):
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


    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and
        messageSender = messageProtocolEntity.getFrom()
        # print 'message participants:', messageProtocolEntity.getParticipant()
        try:
            message = messageProtocolEntity.getBody()

            if messageProtocolEntity == self.resetmsg:
                self.reinitialize()
                if self.resetSendersConversationState(messageSender):
                    print 'conversation state has been reset'

            questionmatches = self.findMessageQuestionMatches(messageSender, message)
            if questionmatches:
                for question in questionmatches:
                    isFirstQuestionBool = self.isFirstQuestion(question)
                    isFollowUpQuestionBool = self.isFollowUpQuestion(messageSender, question)
                    isUserRegisteredInConversationStateBool = self.isUserRegisteredInConversationState(messageSender)
                    hasConversationTimedOutBool = self.hasConversationTimedOut(messageSender, question)

                    shouldReceiveResponse = self.shouldGetResponse(isFirstQuestionBool,
                    isUserRegisteredInConversationStateBool, isFollowUpQuestionBool, hasConversationTimedOutBool)
                    print 'should receive response?', shouldReceiveResponse
                    if shouldReceiveResponse:
                        response = self.findMatchingResponse(question)
                        isConvStateUpdated = self.updateConversationState(messageSender, question)
                        print response, '\n conv state updated: ',isConvStateUpdated, '\n'

                        outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                            response.text,
                            to = messageProtocolEntity.getFrom())
                        self.toLower(outgoingMessageProtocolEntity)

            except Exception, e:
                print 'exception lukt not, ', e



        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())


        # else:
        #     outgoingMessageProtocolEntity = TextMessageProtocolEntity(
        #         messageProtocolEntity.getBody(),
        #         to = messageProtocolEntity.getFrom())

        self.toLower(receipt)
        # uncomment to send msg defined in outgoingMessageProtocolEntity
        # self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)

    #Test. IQ info: http://xmpp.org/rfcs/rfc6120.html#stanzas-semantics-iq
    @ProtocolEntityCallback("iq")
    def onIq(self, entity):
        print(entity)
