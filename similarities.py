# this class has different functions to calculate string and semantic similarities.

#imports
#import enchant
import numpy as np
from sentence_transformers import SentenceTransformer
sbert= SentenceTransformer('bert-base-nli-mean-tokens')


class Similarity:

    def __init__(self):
        pass

    def jaccard_similarity(self,list1, list2):
        s1 = set(list1)
        s2 = set(list2)
        jac= float(len(s1.intersection(s2)) / len(s1.union(s2)))
        if jac >0.8:
            return jac
        return 0


    def cosine_similarity(u, v):
        return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


    def sbert_similarity(self,query, questions):
        #print('__________________________________')
        #print("query:",query)
        #print("questions:",questions)

        q_embed = sbert.encode(query)[0]        #print("q_embed=",q_embed)

        for q in questions:
            #print("q = ",q)
            v=sbert.encode([q])[0]
            #print("v=",v)
            sim = Similarity.cosine_similarity(q_embed,v )

        #    print("Sentence = ", q, "; similarity = ", sim)
            if sim > 0.7:
                return sim
        return 0


    def levenshtein(query, questions):
        for q in questions:
            l_distance=enchant.utils.levenshtein(query, q)
            if l_distance/len(q) <0.8:
                return (1-l_distance)
        return 0
