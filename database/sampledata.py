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
        { "r_nr" : 1, "text" : "doei 1", "conv_id" : 1, "response_to_q_id" : 1},
        { "r_nr" : 2.1, "text" : "doei 21", "conv_id" : 1, "response_to_q_id" : 2.1},
        { "r_nr" : 2.2, "text" : "doei 22", "conv_id" : 1, "response_to_q_id" : 2.2},
        { "r_nr" : 2.3, "text" : "doei 23", "conv_id" : 1, "response_to_q_id" : 2.3},
        { "r_nr" : 3, "text" : "doei 3", "conv_id" : 1, "response_to_q_id" : 3},
        { "r_nr" : 1, "text" : "doei c1", "conv_id" : 2, "response_to_q_id" : 1},
        { "r_nr" : 2, "text" : "doei c2", "conv_id" : 2, "response_to_q_id" : 1},
        { "r_nr" : 1, "text" : "conv3 response", "conv_id" : 3, "response_to_q_id" : 1}
    ]

    convs = [
        { "conv_id" : 1, "conv_name" : "first chat"},
        { "conv_id" : 2, "conv_name" : "second chat"},
        { "conv_id" : 2, "conv_name" : "third chat"}
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
