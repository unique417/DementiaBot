import random
from generators.response_generator_base_class import ResponseGenerator

class ConversationStarterResponseGenerator(ResponseGenerator):
    def __init__(self, filename='conversation_starters.txt'):
        self.filename = filename

    def name(self):
        return "conversation_starter"

    def response(self,text):
        topic = self.input_data['topic']
    
        lines = open('generators/conversation_starters/'+self.filename)
        lines = [ l.strip() for l in lines ]
    
        active_topic = ''
        responses = []
        for l in lines:

            if len(l) < 3:
                continue

            if l[0] == '#':
                continue
    
            if l[0] == '[':
                if l[1:len(topic)+1] == topic:
                    active_topic = topic
                else:
                    active_topic = ''
                continue

            if active_topic == topic:
                responses.append(l)

        if len(responses)>0:
            #return {'response': random.choice(responses)}
            random.shuffle(responses)
            return {'response': responses[:5]}
        else:
            return {'response': ""}
