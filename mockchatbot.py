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





def askForInput():
    try:
        input = raw_input("Your chat message:\n")
        print input
    except Exception, e:
        print 'error:', e

askForInput()
