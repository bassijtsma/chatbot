from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from database.sampledata                               import Sampledata
from database.db                                       import Db
from datetime                                          import time, tzinfo, datetime, timedelta
from incomingMessageHandler                            import IncomingMessageHandler
import datetime as dt
import time
import re


#TODO in case of constant disconnects:
# Event listener that listens to disconnects, and attempt reconnect
# org.openwhatsapp.yowsup.event.network.disconnected
# verify if reconnecting on discnonecting is feasible. something like:
# https://github.com/tgalal/yowsup/issues/921

class EchoLayer(YowInterfaceLayer):
    incomingincomingMessageHandler = incomingMessageHandler()

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #responses =  [{ 'responsetext' : 'responsetext'}, {'responsetext' : 'responsetext'} ]
        responses = incomingincomingMessageHandler.getResponsesForMessage(messageProtocolEntity)

        for response in responses:
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(response['text'],
                to = messageProtocolEntity.getFrom())
            self.toLower(outgoingMessageProtocolEntity)

        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
        self.toLower(receipt)


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)

    #Test. IQ info: http://xmpp.org/rfcs/rfc6120.html#stanzas-semantics-iq
    @ProtocolEntityCallback("iq")
    def onIq(self, entity):
        print(entity)
