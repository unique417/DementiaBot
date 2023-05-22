import random

from generators.response_generator_base_class import ResponseGenerator
#from generators.duck_duck_go import DuckDuckGoResponseGenerator
#from generators.eliza import ElizaResponseGenerator
#from generators.emobot import EmoBotResponseGenerator
#from generators.precanned.precanned import PrecannedResponseGenerator
from generators.conversation_starters.conversation_starters import ConversationStarterResponseGenerator
from generators.greeter import GreeterResponseGenerator
from generators.ai21 import Ai21ResponseGenerator
#from generators.Dialogpt import DialoGPResponseGenerator
#from generators.dementia import Dementia
from generators.gpt3 import Gpt3
#from generators.chatwithhistory_bert import ChatResponseGenerator_Bert
#from generators.chatwithhistory_KNN import ChatResponseGenerator_KNN
#from generators.chatwithhistory_KQs import ChatResponseGenerator_KQs
#from generators.chatwithhistory_gpt2 import ChatResponseGenerator_gpt2
#from generators.chatwithhistory_dict import ChatResponseGenerator_dict

base = ResponseGenerator()
#duckduckgo = DuckDuckGoResponseGenerator()
#eliza = ElizaResponseGenerator()
#emobot = EmoBotResponseGenerator()
#precanned = PrecannedResponseGenerator('sentences_critical.txt')
#precanned_witty = PrecannedResponseGenerator('sentences_witty.txt')
ai21=Ai21ResponseGenerator()
conversation_starter = ConversationStarterResponseGenerator()
greeter = GreeterResponseGenerator()
#dialogpt = DialoGPResponseGenerator()
#dementia = Dementia()
gpt3 = Gpt3()


response_generators = [ai21,gpt3]

if __name__=="__main__":
    sample_texts = ["I'm having a bad day", "I feel so sad.", "Tell me about cats", "What is minecraft", "minecraft", "are you a robot", "I just want to die"]
    response_generators = [greeter]
    response = ""
    for g in response_generators:
        print('\n'+g.name())
        for t in sample_texts:
            g.input_data = {"previous_response":response,
                            "handpicked_keywords":[random.choice(t.split())],
                            "topic":'books',
                            "strict_topic":'books',
                            "ner": {},
                            "key_phrases":[random.choice(t.split())],
                            "text":t}
            response = g.response(t)['response']
            print('  DementiaBot: '+response)
