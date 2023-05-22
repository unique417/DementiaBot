import sys
from conversation_engine import conversation_engine
#from emotion_detector import Emotion
from personality_questions import MBTIClassifier
#from stanford_triple_extraction import StanfordOpenIEWrapper
from similarities import Similarity
from yes_no import Yes_no
from knowledgegraph import KnowledgeGraph

#emotion= Emotion()
ce = conversation_engine()
mbti= MBTIClassifier()
#stanford_triple_extractor = StanfordOpenIEWrapper()
sim= Similarity()
kg=KnowledgeGraph()
ynclassifier = Yes_no()
response = ce.start()
start_sent=response
flag=0
personality=[" - "," - "," - "," - "]
done=False

while(1):
    text = input(response+'\n')
    #print("FLAG = *******************************" ,flag)
    if flag != 0:
        #check if the response is yes or no.
        yn=ynclassifier.classifier(text)
        #print("yn = *******************************" ,yn)

        #send the yes or no response and flag to mbti.personality_classifier
        personality,done =ce.personality_classifier(yn,flag)
        flag=0
    q,flag=ce.flag(text)
    #print("question= ",q)
    print("User's personality so far :", personality)
    if done== True:
        kg.add_personality(personality)

    #relevant_triples = sim.sbert_similarity(text,kg.get_all_triples())
    #extract information:

    #knowledge=stanford_triple_extractor.extract_triples(text)
    #for triple in knowledge:
    #    kg.add_edge(triple)

#    mo= emotion.get_emotion(text)

    response = ce.chat(text,q, verbose=True)

    print("DementiaBot :", response)
