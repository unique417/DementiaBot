import random
import numpy as np

import generators.response_generators as generators
import evaluators.response_evaluators as evaluators
import nlp_pipeline.pipeline as pipeline
from similarities import Similarity
from personality_questions import MBTIClassifier

class conversation_engine:

    def __init__(self, nlp=None, selected_generators=None, selected_evaluators=None, selected_filters=None, verbose=False):
        self.response_generators = selected_generators if selected_generators else generators.response_generators
        self.evaluators = selected_evaluators if selected_evaluators else evaluators.response_evaluators
        self.filters = selected_filters if selected_filters else evaluators.response_filters
        self.pipeline = nlp if nlp else pipeline.nlp_modules
        #print("Active Generators:", [g.name() for g in self.response_generators])
        #print("Active Rankers:", [e.name() for e in self.evaluators])
        self.context = {}
        self.context['history'] = []
        self.E=0
        self.I=0
        self.S=0
        self.N=0
        self.T=0
        self.F=0
        self.J=0
        self.P=0
        self.personality=[" - "," - "," - "," - "]
        self.done= False
        self.counter=0
        self.sentence_counter = 0

        self.cat_E = ['I feel like socializing can make you energized. Do you have enough time for socializing?','You are very friendly! I like talking to you a lot!’,’I like that you can share your thoughts and emotions. This is an important skill and not everyone has it.']
        self.cat_I = ['If you are feeling down, maybe some inside time can help you feel better. Read a few pages of a book if you have time.','Have you ever thought about writing a book? you have a beautiful mind', "I feel like you don't like to be the center of attention, right?"]
        self.cat_S = ['based on what I learned about you, focusing on the present can be best for you. The past is past and too much thinking about the future can make you stressed.','I like how you notice small things that others might simply ignore.', 'Have you ever thought about becoming a detective? I see that you have a hyper sense of observation.']
        self.cat_N = ["If you are feeling stressed, writing down your tasks and planning for the future can make you feel better. This way you'll have each step planned.",'I feel like talking about things in a figurative way, it is almost poetic! I like it :)']
        self.cat_T = ["you are a logical person. I have this feeling that I can trust your decisions!",'I feel like you are a professional overthinker! I see how much you like analyzing facts.']
        self.cat_F = ["I feel like you always follow your heart. That is a good thing. Your heart usually guides you to the best destination.",'I like your sense of morality. you can be a natural peace-maker!']
        self.cat_J = ['you seem like a quick decision maker.','I feel like you are a naturally organized person. Is that because it helps you have things under your control?']
        self.cat_P = ['I learned this about you. You like to approach life in a freewheeling, spontaneous way. I think this is beautiful. Life never gets boring for you :)',"I think you don't like the daily grind of routines. Do you want to learn something new?"]

        self.extraversionVSintroversion = ['Do you usually make friends so easily?','Do you have many friends?',
        "I'm trying to know you better. Do you like spending time with friends rahter than being alone?",
        'I want to know you better, do you consider yourself as an extravert?',
        'Do you feel comfortable around people?',
        'Do you enjoy being a part of a group?']

        #Sensing(S) or intuition(N)? if yes, sensing will get a score.
        self.sensingVSintuition = ['Do you focus more on facts and details before the big picture?',
        'Do you always pay attention to the details?','do you consider yourself as a practical and pragmatic person?',
        'Do you like having a routing in your work rather than imagining possiblities? I ask this question  because I want to know you better.',
        'Are your thought usually present-oriented?'
        ]

        #Thinking (T) or Feeling (F). if yes, feelings get a score
        self.thinkingVSfeeling = ['Do you usually let your feelings affect your decisions?',
        'When you want to do a task, do usually follow your emotions and instincts rather than the rules?',
        'When you want to make a decision, do you usually talk to the people involved?',
        'when it comes to choices, do you usually listen to your heart?',
        'do you consider yourself as an emotional person?'
        ]

        #Judging (J) or Perceiving (P). if yes judging gets a score
        self.judgingVSperceiving = ['You appear to be task oriented, is that right?',
        'Do you like to make lists of things to do?',
        'like to have things decided?',
        'Are you a task-oriented person?',
        'Do you like to schedule things in advance?']

    def start(self):
        response = generators.greeter.response()['response']
        self.context['previous_response'] = response
        return response

    def start_history(self):
        response = "What would you like to know?"
        self.context['previous_response'] = response
        return response

    def run_nlp_pipeline(self, text):
        for module in self.pipeline:
            result = module.process(text, self.context)
            for key in result:
                self.context[key] = result[key]
            #print(module.name(), result)
        print()

    def update_context(self,text):
        self.context['text'] = text
        self.context['history'].append(text)
        self.context['topic'] = ''
        self.run_nlp_pipeline(text)

        # DEPRECATED: these context tags are needed by legacy repsonse generators
        self.context['handpicked_keywords'] = [random.choice(text.split())]
        self.context['strict_topic'] = ''
        self.context['ner'] = {}
        self.context['key_phrases'] = [random.choice(text.split())]

    def argmax_or_rand(self, arr):
        candidates = [0]
        max = arr[0]

        for i, val in enumerate(arr):
            if i == 0:
                continue
            if arr[i] > max:
                candidates = [i]
                max = arr[i]
            elif arr[i] == max:
                candidates.append(i)

        return random.choice(candidates)

    def choose_response(self, responses):
        scores = np.ones(len(responses))
        for evaluator in self.evaluators:
            scores += evaluator.rank(self.context, responses)
        for filter in self.filters:
            scores *= filter.rank(self.context, responses)

        #print("Total scores: ")
        #print(scores)
        #print('\n')
        return responses[self.argmax_or_rand(scores)]

    def flag(self,response):
        ####is text similar to questions?###
        sim=Similarity()
        mbti=MBTIClassifier()
        flag = 0
        allow = 10
        self.counter +=1
        if response[-1]=="?":
            self.counter -=1
        if self.counter == 3:
            allow = random.randint(1,4)
            self.counter = 0

        response=[response]
        while True:
            if sim.sbert_similarity(response,self.extraversionVSintroversion) > 0.7 or allow == 1:
                for q1 in self.extraversionVSintroversion:
                    question = q1
                    flag = 1
                    self.extraversionVSintroversion.remove(q1)

                    return question,flag


            if sim.sbert_similarity(response,self.sensingVSintuition) > 0.7 or allow == 2:
                for q2 in self.sensingVSintuition:
                    question =q2
                    flag = 2
                    self.sensingVSintuition.remove(q2)
                    print("allow 2: ", allow)
                    return question,flag

            if sim.sbert_similarity(response,self.thinkingVSfeeling) > 0.7 or allow == 3:
                for q3 in self.thinkingVSfeeling:
                    question =q3
                    flag = 3
                    self.thinkingVSfeeling.remove(q3)
                    print("allow 2: ", allow)
                    return question,flag

            if sim.sbert_similarity(response,self.judgingVSperceiving) > 0.7 or allow == 4:
                for q4 in self.judgingVSperceiving:
                    question =q4
                    flag = 4
                    self.judgingVSperceiving.remove(q4)
                    print("allow 2: ", allow)
                    return question,flag

            flag = 0
            break
        return None , flag

    def sentences(self,response,personality):
        self.sentence_counter +=1
        if self.sentence_counter % 5 ==0:
            if personality[0] == "E":
                for sen in self.cat_E:
                    response = response +' '+ sen
                    self.cat_E.remove(sen)
                    self.sentence_counter =0
                    return response

            elif personality[0] == "I":
                for sen in self.cat_I:
                    response = response +' '+ sen
                    self.cat_I.remove(sen)
                    self.sentence_counter =0
                    return response

            elif personality[1] == "S":
                for sen in self.cat_S:
                    response = response +' ' + sen
                    self.cat_S.remove(sen)
                    self.sentence_counter =0
                    return response

            elif personality[1] == "N":
                for sen in self.cat_N:
                    response = response +' '+ sen
                    self.cat_N.remove(sen)
                    self.sentence_counter =0
                    return response

            elif personality[2] == "T":
                for sen in self.cat_T:
                    response = response +' '+ sen
                    self.cat_T.remove(sen)
                    self.sentence_counter =0
                    return response

            elif personality[2] == "F":
                for sen in self.cat_F:
                    response = response +' '+ sen
                    self.cat_F.remove(sen)
                    self.sentence_counter =0
                    return response

            elif personality[3] == "J":
                for sen in self.cat_J:
                    response = response +' '+ sen
                    self.cat_J.remove(sen)
                    self.sentence_counter =0
                    return response

            elif personality[3] == "P":
                for sen in self.cat_P:
                    response = response +' '+ sen
                    self.cat_P.remove(sen)
                    self.sentence_counter =0
                    return response
        return response


    def personality_classifier(self,yn,flag):

        if yn=="yes":
            if flag ==1:
                self.E +=1
            elif flag==2:
                self.S +=1
            elif flag==3:
                self.F +=1
            elif flag ==4:
                self.J +=1
        elif yn=="no":
            if flag ==1:
                self.I +=1
            elif flag==2:
                self.N +=1
            elif flag==3:
                self.T +=1
            elif flag ==4:
                self.P +=1
        else:
            return self.personality ,self.done
        if self.E !=0 or self.I !=0:
            self.personality[0] = "E" if self.E>self.I else "I"
        if self.S !=0 or self.N !=0:
            self.personality[1] = "S" if self.S>self.N else "N"
        if self.F !=0 or self.T !=0:
            self.personality[2] = "F" if self.F>self.T else "T"
        if self.J !=0 or self.P !=0:
            self.personality[3] = "J" if self.J >self.P else "P"



        if len(self.sensingVSintuition)==0 and len(self.extraversionVSintroversion)==0 and len(self.thinkingVSfeeling)==0 and len(self.judgingVSperceiving)==0:
             self.done= True

        return self.personality ,self.done


    def chat(self, text, question, verbose):
        self.update_context(text)
        #responses = ["I'm not sure what to say."]
        responses = []
        sources = []

        for g in self.response_generators:
            g.input_data = self.context
            g.context = self.context
            response = g.response(text)['response']
            #print(g.name())
            #print(response)
            #if verbose:
            #    print('   '+g.name()+": ",response)

            if response:
                if isinstance(response, str):
                    #generator returned a single response
                    responses.append(response)
                    sources.append(g.name())
                    #print("22222222222222222222222222")
                else:
                    #generator returned a list of possible responses
                    responses += response
                    sources += [g.name]*len(response)
                    #print("3333333333333333333333333333")

        response = self.choose_response(responses)
        #print("44444444444444444444444444")
        if question != None:
            response += question
        self.context['previous_response'] = response
        #print("555555555555555555555555555")
        return response
