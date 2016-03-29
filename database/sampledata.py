#!/usr/bin/python

class Sampledata:

    def getQuestions(self):
        return self.q

    def getResponses(self):
        return self.r

    def getConversations(self):
        return self.convs

    def getTestconversationState(self):
        return self.testconversationstate

    def getMessages(self):
        return self.messages

    q = [
        { "q_nr" : 1, "text" : "hoi1", "conv_id" : 1},
        { "q_nr" : 2.1, "text" : "hoi21", "conv_id" : 1},
        { "q_nr" : 2.2, "text" : "hoi22", "conv_id" : 1},
        { "q_nr" : 2.3, "text" : "hoi23", "conv_id" : 1},
        { "q_nr" : 3, "text" : "hoi3", "conv_id" : 1},
        { "q_nr" : 1, "text" : "hoic1", "conv_id" : 2},
        { "q_nr" : 2, "text" : "hoic2", "conv_id" : 2},
        { "q_nr" : 1, "text" : "conv3", "conv_id" : 3}
    ]

    r = [
        { "r_nr" : 1, "text" : "doei 1", "conv_id" : 1, "response_to_q" : 1},
        { "r_nr" : 2.1, "text" : "doei 21", "conv_id" : 1, "response_to_q" : 2.1},
        { "r_nr" : 2.2, "text" : "doei 22", "conv_id" : 1, "response_to_q" : 2.2},
        { "r_nr" : 2.3, "text" : "doei 23", "conv_id" : 1, "response_to_q" : 2.3},
        { "r_nr" : 3, "text" : "doei 3", "conv_id" : 1, "response_to_q" : 3},
        { "r_nr" : 1, "text" : "doei c1", "conv_id" : 2, "response_to_q" : 1},
        { "r_nr" : 2, "text" : "doei c2", "conv_id" : 2, "response_to_q" : 1},
        { "r_nr" : 1, "text" : "conv3 response", "conv_id" : 3, "response_to_q" : 1}
    ]

    convs = [
        { "conv_id" : 1, "conv_name" : "first chat"},
        { "conv_id" : 2, "conv_name" : "second chat"},
        { "conv_id" : 3, "conv_name" : "third chat"}
    ]

    # TODO
    # REFACTOR new combined data structure for simplicity in frontend

    messages = [
     { "message_id": 1, "q_nr" : 1, "r_nr" : 1, "qtext" : "hoi1", "rtext" : "doei 1", "is_alternative" : False, "conv_id" : 1 },
     { "message_id": 2, "q_nr" : 2, "r_nr" : 2, "qtext" : "hoi21", "rtext" : "doei 21", "is_alternative" : True, "conv_id" : 1 },
     { "message_id": 3, "q_nr" : 2, "r_nr" : 2, "qtext" : "hoi22", "rtext" : "doei 22", "is_alternative" : True, "conv_id" : 1 },
     { "message_id": 4, "q_nr" : 2, "r_nr" : 2, "qtext" : "hoi23", "rtext" : "doei 23", "is_alternative" : True, "conv_id" : 1 },
     { "message_id": 5, "q_nr" : 3, "r_nr" : 3, "qtext" : "hoi3", "rtext" : "doei 3", "is_alternative" : False, "conv_id" : 1 },
     { "message_id": 6, "q_nr" : 1, "r_nr" : 1, "qtext" : "hoic21", "rtext" : "doei c21", "is_alternative" : False, "conv_id" : 2 },
     { "message_id": 7, "q_nr" : 2, "r_nr" : 2, "qtext" : "hoic22", "rtext" : "doei c22", "is_alternative" : False, "conv_id" : 2 },
     { "message_id": 8, "q_nr" : 1, "r_nr" : 1, "qtext" : "hoic31", "rtext" : "doei c31", "is_alternative" : False, "conv_id" : 3 },
    ]



    testconversationstate = {
        123 : [
            {'conv_id': 1, 'latestinteraction' : 10, 'mostrecentquestion': 2.2 },
            {'conv_id': 2, 'latestinteraction' : 30, 'mostrecentquestion': 2 },
        ],
        456 : [
            {'conv_id': 2, 'latestinteraction' : 44, 'mostrecentquestion': 1 },
            {'conv_id': 3, 'latestinteraction' : 30, 'mostrecentquestion': 5 },
            {'conv_id': 1, 'latestinteraction' : 2, 'mostrecentquestion': 3 },
        ],
        789 : [
            {'conv_id': 5, 'latestinteraction' : 21, 'mostrecentquestion': 1 },
            {'conv_id': 4, 'latestinteraction' : 30, 'mostrecentquestion': 1 },
            {'conv_id': 1, 'latestinteraction' : 2, 'mostrecentquestion': 3 },
        ]
    }
