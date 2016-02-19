from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from database.db                                       import Db



#TODO
# reset functie maken. 'chat reset' zet het gesprek weer op 0
#
# event listener die luisterd naar disconnect, en weer verbinding maakt
# org.openwhatsapp.yowsup.event.network.disconnected
# verify if reconnecting on discnonecting is feasible. something like: https://github.com/tgalal/yowsup/issues/921

class EchoLayer(YowInterfaceLayer):
    database = Db()
    questions = database.getQuestions()
    responses = database.getResponses()


    def reinitialize(self):
        print 'resetting questions and responses...'
        self.questions = database.getQuestions()
        self.responses = database.getResponses()

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and
        print 'message van:', messageProtocolEntity.getFrom()
        print 'message participants:', messageProtocolEntity.getParticipant()
        print messageProtocolEntity.getBody()

        if messageProtocolEntity.getBody() == 'chat reset':
            self.reinitialize()

        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
        messagebody = messageProtocolEntity.getBody().lower()

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
