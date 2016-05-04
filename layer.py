from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from database.sampledata                               import Sampledata
from database.db                                       import Db
from datetime                                          import time, tzinfo, datetime, timedelta
from responseBuilder                                   import ResponseBuilder
from yowsup.layers.network                             import YowNetworkLayer
from yowsup.layers                                     import YowLayerEvent
import datetime as dt
import time
import re



class EchoLayer(YowInterfaceLayer):
    responseBuilder = ResponseBuilder()

    def onEvent(self, layerEvent):
        # In case of constant disconnects.  https://github.com/tgalal/yowsup/iss
        print 'event:', layerEvent.getName()
        if layerEvent.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECTED:
            print "Disconnected- %s" % layerEvent.getArg("reason")
            self.getStack().broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
            print 'reconnected'
            # self.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))


    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #responses =  [{ 'responseText' : 'responsetext'}, {'responseText' : 'responsetext'} ]
        responses = self.responseBuilder.getResponsesForMessage(messageProtocolEntity)

        for response in responses:
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(response['responseText'],
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
