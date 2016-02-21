from database.sampledata import Sampledata

# Requirements:

# 1. User provides a message (question), bot responds
# 2a. User can ask a follow up question, and bot responds as a follow up
# 2b. The bot does not respond the follow up unless the first question has also been asked
# 3a. User can ask an alternative follow up question, providing several different answers
# 3b. Each alterantive question has its respective answer, even if the content of the answer is the same
# 4a. Defined messages (questions) should be transformed to lower case
# 4b. An input given by the user during the chat should be transformed to Lower case
# 5. All the words in the given input during the chat should be checked against the defined messages (questions)

# Nice to Haves:
# 1. Discard determiners (lidwoorden)
# 2. Performing stemming on given input

sampledata = Sampledata()
questions = sampledata.getQuestions()
responses = sampledata.getResponses()
conversations = sampledata.getConversations()

# Keeps track of the state of different conversations, so different people
# can talk to the bot at the same time without the chat intermingling a response
# messageProtocolEntity.getFrom() will be key.The most recent interaction with
# the bot will be tracked to figure out if the conversation has timed out and
# should be reset. Finally, it tracks how far into the conversation they are.
# conversationstate =
    # {   m.getFrom() : {
    #         latestInteraction : timestamp,
    #         mostrecentquestion: question_nr },
    #     m.getFrom() : {
    #         latestInteraction : timestamp,
    #         mostrecentquestion: question_nr },
    #     m.getFrom() : {
    #         latestInteraction : timestamp,
    #         mostrecentquestion: question_nr },
    # }

conversationstate = []

print questions
print responses
print conversations

def askForInput():
    input = raw_input("Your chat message:\n")
    print input
    return input


def defineConvId():
    input = raw_input("\nWhats the conv id?\n")
    try:
        conv_id = int(input)
    except:
        print 'invalid conv id'
        exit()
    return conv_id


def getConvName(conv_id):
    for conv in conversations:
        if conv_id == conv['conv_id']:
            print 'the conv name is:', conv['conv_name']
            return conv['conv_name']


# TODO: decide what method of time handling to use
# must be able to delta different timestamps
def updateConversationState(messageSender, question_nr):
    conversationstate[messageSender][latestInteraction] = 0 #TODO timestamp
    conversationstate[messageSender][question_nr] = question_nr


conv_id = defineConvId()
conv_name = getConvName(conv_id)
while True:
    askForInput()
