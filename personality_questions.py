#this class contains questions which scores how much user's personality is leaning toward one of the characteristics in each pair

import random


class MBTIClassifier:

    def __init__(self):
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
        self.extraversionVSintroversion = ['Do you usually make friends so easily?',
        'Do you have many friends?',
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
        'When you want to do a task, do usually follow your emotions and instincts ratherr than the rules?',
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


    def response(self, text, cat):
        #cat shows which category does the user input belongs to. we return a response from the same category.

        #Extravert(E) or introvert(I)? if yes, extravert gets a score.



        """if cat==0:
            if len(extraversionVSintroversion)==0:
                return None
            resp = random.choice(extraversionVSintroversion)
            extraversionVSintroversion.drop(resp)
        elif cat==1:
            if len(sensingVSintuition)==0:
                return None
            resp = random.choice(sensingVSintuition)
            sensingVSintuition.drop(resp)
        elif cat==2:
            if len(thinkingVSfeeling)==0:
                return None
            resp = random.choice(thinkingVSfeeling)
            thinkingVSfeeling.drop(resp)
        elif cat==3:
            if len(judgingVSperceiving)==0:
                return None
            resp = random.choice(judgingVSperceiving)
            judgungVSperceiving.drop(resp)"""
        #return {"response": resp}

    def personality_classifier(self,yn,flag):
        if yn=="yes":
            if flag ==1:
                self.E +=1
            elif flag==2:
                self.S +=1
            elif flag==3:
                self.F +=1
            else:
                self.J +=1
        elif yn=="no":
            if flag ==1:
                self.I +=1
            elif flag==2:
                self.N +=1
            elif flag==3:
                self.T +=1
            else:
                self.P +=1
        if self.E !=0 or self.I !=0:
            self.personality[0] = "E" if self.E>self.I else "I"
        if self.S !=0 or self.N !=0:
            self.personality[1] = "S" if self.S>self.N else "N"
        if self.F !=0 or self.T !=0:
            self.personality[2] = "F" if self.F>self.T else "T"
        if self.J !=0 or self.P !=0:
            self.personality[3] = "J" if self.J >self.P else "P"

        else:
            pass

        if len(sensingVSintuition)==0 and len(extraversionVSintroversion)==0 and len(thinkingVSfeeling)==0 and len(judgingVSperceiving)==0:
             self.done= True

        return self.personality ,self.done



    def name(self):
        return str(type(self))
