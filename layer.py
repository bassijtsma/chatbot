from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity



class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over

        print 'on message werkt'
        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())

            print messageProtocolEntity.getBody()

            messagebody = messageProtocolEntity.getBody().lower()
            naam = 'rutger'
            naamtwo = 'kees'
            if (naam in messagebody) or (naamtwo in messagebody):

                outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                    'HELEMAAL GEK!!',
                    to = messageProtocolEntity.getFrom())

                self.toLower(outgoingMessageProtocolEntity)

            elif messagebody == "ik heb zin in pizza":
                returnmessage = "Als t maar geen dominos is"
                outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                    returnmessage,
                    to = messageProtocolEntity.getFrom())
                self.toLower(outgoingMessageProtocolEntity)

            elif messagebody == "ik heb zin in doner":
                returnmessage = "AIJT NAAR T EETHUIS"
                outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                    returnmessage,
                    to = messageProtocolEntity.getFrom())
                self.toLower(outgoingMessageProtocolEntity)
            # else:
            #     outgoingMessageProtocolEntity = TextMessageProtocolEntity(
            #         messageProtocolEntity.getBody(),
            #         to = messageProtocolEntity.getFrom())
            else:
                print 'msg not soeters or pizza'

            self.toLower(receipt)
            # self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
