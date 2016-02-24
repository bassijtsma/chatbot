# chatbot
Test implementation of a chatbot



# Implemented:
1. User provides a message (question), bot responds
2a. User can ask a follow up question, and bot responds with a follow up response
2b. The bot does not respond the follow up unless the previous question has also been asked
3a. User can ask an alternative follow up question, providing several different answers
3b. Each alternative question has its respective answer, even if the content of the (alternative) answer is the same
4a. Defined questions should be transformed to lower case to ensure case insensitivity
4b. An input given by the user during the chat should be transformed to Lower case to ensure case insensitivity
5. All the words in the given input during the chat should be checked against the defined messages (questions)
6. Users can have multiple conversations with a chatbot at the same time
