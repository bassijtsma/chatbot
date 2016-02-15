from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from database.db                                       import Db


class EchoLayer(YowInterfaceLayer):
    textcounter = 0
    database = Db(test)

    database.getQuestions()
    database.getResponses()

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):


        #send receipt otherwise we keep receiving the same message over and over
        print 'on message werkt'
        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())

            # can keep state within the echoLayer class in the Loop
            self.textcounter += 1
            print textcounter
            print messageProtocolEntity.getBody()

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
