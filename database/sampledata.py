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

    # oldquestions = [
    #     { "qid" : 1, "text" : "hoi", "conv_id" : 1, 'question_to' : [{ "rid" : "1" }] },
    #     { "qid" : 2, "text" : "dubbel hoi", "conv_id" : 1, 'question_to' : [{ "rid" : "2"  }] },
    #     { "qid" : 3, "text" : "drie", "conv_id" : 1, 'question_to' : [{ "rid" : "2" }] },
    #     { "qid" : 1, "text" : "een conv2", "conv_id" : 2 }
    # ]

    # oldresponses = [
    #     { "rid" : 1, "text" : "doei1antw", "conv_id" : 1, "response_to" : [ { "qid" : 1 } ] },
    #     {  "rid" : 2, "text" : "doei23antw", "conv_id" : 1, "response_to" : [ { "qid" : 1 }, { "qid" : 2 }, { "qid" : 3 } ] }
    # ]


    q = [
        { "qnr" : 1, "text" : "hoi", "conv_id" : 1},
        { "qnr" : 2.1, "text" : "hoi21", "conv_id" : 1},
        { "qnr" : 2.2, "text" : "hoi22", "conv_id" : 1},
        { "qnr" : 2.3, "text" : "hoi23", "conv_id" : 1},
        { "qnr" : 3, "text" : "hoi3", "conv_id" : 1},
        { "qnr" : 1, "text" : "hoic1", "conv_id" : 2},
        { "qnr" : 2, "text" : "hoic2", "conv_id" : 2}
    ]

    r = [
        { "rnr" : 1, "text" : "doei 1", "conv_id" : 1, "response_to_q" : 1},
        { "rnr" : 2.1, "text" : "doei 21", "conv_id" : 1, "response_to_q" : 2.1},
        { "rnr" : 2.2, "text" : "doei 22", "conv_id" : 1, "response_to_q" : 2.2},
        { "rnr" : 2.3, "text" : "doei 23", "conv_id" : 1, "response_to_q" : 2.3},
        { "rnr" : 3, "text" : "doei 3", "conv_id" : 1, "response_to_q" : 3},
        { "rnr" : 1, "text" : "doei c1", "conv_id" : 2, "response_to_q" : 1},
        { "rnr" : 2, "text" : "doei c2", "conv_id" : 2, "response_to_q" : 1}
    ]

    convs = [
        { "conv_id" : 1, "conv_name" : "eerste gesprek"},
        { "conv_id" : 2, "conv_name" : "tweede gesprek"}
    ]


    testconversationstate = {
        123 : [
            {'conv_id': 1, 'latestinteraction' : 10, 'mostrecentquestion': 5 },
            {'conv_id': 5, 'latestinteraction' : 30, 'mostrecentquestion': 2 },
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
