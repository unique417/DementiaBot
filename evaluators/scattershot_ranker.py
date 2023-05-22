import numpy as np
from scipy import spatial

#from embeddings.embedder import embed, list_embed
from evaluators.ranker_base_class import Ranker

import chitchat_dataset as ccc

import spacy
nlp = spacy.load("en_core_web_sm")

def embed(text):
    doc = nlp(text)
    return doc.vector

def list_embed(texts):
    embeddings = []
    for text in texts:
        embeddings.append(embed(text))
    return embeddings

# This ranker maintains its scaffold corpus as a list of conversations,
# each of which contains a list of (embedded) messages

# In the chitchat dataset, conversations do not necessarily alternate
# between speakers with each new message. This fact is ignored in the
# current version, on the assumption that subsequent posts by the same
# speaker will likely follow similar trends.

class ScattershotRanker(Ranker):
    def __init__(self, scaffold_corpus="chitchat"):
        self.load_scaffold(scaffold_corpus)

    def name(self):
        return "Scattershot Ranker"

    def find_scaffold_match(self, v_context, num_matches=1):
        # find scaffold entry that most closely matches v_context[-1]

        vectors = np.vstack(np.array(self.scaffold))
        distances = spatial.distance.cdist([v_context[-1]], vectors, metric='cosine')
        inds = np.argsort(distances)
        return self.scaffold[inds[0][0]] # For now, just take the top match

    def rank(self, context, sentences):
        chat_history = context['history'][-2:] # for now, only use a context of len 2

        v_context = list_embed(chat_history)
        v_sentences = list_embed(sentences)
        v_scaffold = self.find_scaffold_match(v_context)

        # calculate distances from each sentence to v_scaffold
        distances = spatial.distance.cdist([v_scaffold],np.vstack(v_sentences),metric='cosine')
        scores = 2-distances[0]
        #print(scores)
        return scores

    def load_scaffold(self, corpus, LIMIT=20):
        self.scaffold = []
        #print('loading corpus for scattershot ranker...')
        #print('scattershot number-of-conversations limit is', LIMIT)
        if corpus == "chitchat":
            dataset = ccc.Dataset()
            for convo_id, convo in list(dataset.items())[:LIMIT]:
                messages = []
                for message in convo["messages"]:
                    for line in message:
                        messages.append(line["text"])
                #print(messages)
                #input('>')
                self.scaffold += list_embed(messages)
                #print("done embedding")
        else:
            raise ValueError("Unknown scaffold corpus for Scattershot Ranker: " + corpus)
        print(len(self.scaffold), 'sentences embedded.')
        if not self.scaffold:
            raise ValueError("Unknown error while loading scaffold corpus. No conversations retrieved.")

if __name__=="__main__":
    r = ScattershotRanker()
    context = ['Hello, my name is Nancy.']
    sentences = ['That is a strange thing to say', 'Pleased to meet you!', 'fish are aquatic animals with scales and gills.',"Hi there! I'm Eve.","So what are we supposed to talk about?","Have you seen the movie Iron Man?"]
    r.rank(context, sentences)
