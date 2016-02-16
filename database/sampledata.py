questions = {[
    { "qid" : 1, "text" : "hoi", "conv_id" : 1, 'question_to' : [{ "rid" : "1" }] },
    { "qid" : 2, "text" : "dubbel hoi", "conv_id" : 1, 'question_to' : [{ "rid" : "2"  }] },
    { "qid" : 3, "text" : "drie", "conv_id" : 1, 'question_to' : [{ "rid" : "2" }] },
    { "qid" : 1, "text" : "een conv2", "conv_id" : 2 }
]}

responses = {[
    { "rid" : 1, "text" : "doei1antw", "conv_id" : 1, "response_to" : [ { "qid" : 1 } ] },
    {  "rid" : 2, "text" : "doei23antw", "conv_id" : 1, "response_to" : [ { "qid" : 1 }, { "qid" : 2 }, { "qid" : 3 } ] }
}]
