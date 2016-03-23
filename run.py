from layer import EchoLayer
from yowsup.layers                             import YowParallelLayer
from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.stanzaregulator             import YowStanzaRegulator
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.protocol_iq                 import YowIqProtocolLayer
from yowsup.layers.protocol_calls              import YowCallsProtocolLayer
from yowsup.layers.logger                      import YowLoggerLayer
from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup.layers.axolotl                     import YowAxolotlLayer
from yowsup import env

try:
    import credentials as crdntials
except Exception:
    print '''Your phone nr credentials could not be loaded. Read the instructions
             in the credentials_todo.py file. Don't forget to rename the file
             to credentials.py'''

crdntls = crdntials.Credentials()
CREDENTIALS = (crdntls.getlogin(), crdntls.getpassword())

if __name__==  "__main__":
    layers = (
        EchoLayer,
    #     YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowMediaProtocolLayer, YowIqProtocolLayer, YowCallsProtocolLayer]),YowAxolotlLayer
    # ) + YOWSUP_CORE_LAYERS
    YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowMediaProtocolLayer, YowIqProtocolLayer, YowCallsProtocolLayer]),
    YowAxolotlLayer,
    YowLoggerLayer,
    YowCoderLayer,
    YowCryptLayer,
    YowStanzaRegulator,
    YowNetworkLayer)

    stack = YowStack(layers)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)         #setting credentials
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])    #whatsapp server address
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())          #info about us as WhatsApp client

    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal

    print 'going into stack loop'
    stack.loop(timeout = 15, discrete = 15) #this is the program mainloop
    print 'stack loop finished'
