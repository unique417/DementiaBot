class MBTIResponseGenerator:

    def __init__(self):
        pass

    def response(self, text, cat):
        #cat shows which category does the user input belongs to. we return a response from the same category.

        #Extravert(E) or introvert(I)? if yes, extravert gets a score.
        extraversionVSintroversion = ['Do you usually make friends so easily?',
        'Do you have many friends?',
        "I'm trying to know you better. Do you like spending time with friends rahter than being alone?",
        'I want to know you better, do you consider yourself as an extravert?',
        'Do you feel comfortable around people?',
        'Do you enjoy being a part of a group?']

        #Sensing(S) or intuition(N)? if yes, sensing will get a score.
        sensingVSintuition = ['I focus more on facts and details before the big picture.',
        'Do you always pay attention to the details?','do you consider yourself as a practical and pragmatic person?',
        'Do you like having a routing in your work rather than imagining possiblities? I ask this question  because I want to know you better.',
        'Are your thought usually present-oriented?'
        ]

        #Thinking (T) or Feeling (F). if yes, feelings get a score
        thinkingVSfeeling = ['Do you usually let your feelings affect your decisions?',
        'When you want to do a task, do usually follow your emotions and instincts ratherr than the rules?',
        'When you want to make a decision, do you usually talk to the people involved?',
        'when it comes to choices, do you usually listen to your heart?',
        'do you consider yourself as an emotional person?'
        ]

        #Judging (J) or Perceiving (P). if yes judging gets a score
        judgungVSperceiving = ['You appear to be task oriented, is that right?',
        'Do you like to make lists of things to do?',
        'like to have things decided?',
        'Are you a task-oriented person?',
        'Do you like to schedule things in advance?']


        if cat==0:
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
            if len(judgungVSperceiving)==0:
                return None
            resp = random.choice(judgungVSperceiving)
            judgungVSperceiving.drop(resp)
        return {"response": resp}

    def name(self):
        return str(type(self))
