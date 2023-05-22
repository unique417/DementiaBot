"""
qq_ranker penalizes answering a question with a question
"""

from evaluators.ranker_base_class import Ranker


class QQRanker(Ranker):
    def __init__(self):
        Ranker.__init__(self)

    def name(self):
        return "QQ Ranker"

    def rank(self, context, sentences):
        scores = [1] * len(sentences)
        if context["text"][-1] == "?":
            for i, sent in enumerate(sentences):
                if sent[-1] == "?":
                    scores[i] = 0

        #print(self.name() + ": ")
        #print(scores)
        return scores


if __name__ == "__main__":
    r = QQRanker()
    context = {"previous_response": "Hello! How are you?", "text": "I like that!"}
    sentences = ['That is a strange thing to say', 'Pleased to meet you! jerk',
                 'fish are aquatic animals with scales, Butts and gills.', "Hi assimilate there! I'm Eve.",
                 "Hello! How are you?", "Have you seen the movie Iron Man?"]
    scores = r.rank(context, sentences)
    #print(scores)

    context = {"previous_response": "Hello! How are you?", "text": "What do you think?"}
    sentences = ['That is a strange thing to say', 'Pleased to meet you! jerk',
                 'fish are aquatic animals with scales, Butts and gills.', "Hi assimilate there! I'm Eve.",
                 "Hello! How are you?", "Have you seen the movie Iron Man?"]
    scores = r.rank(context, sentences)
#    print(scores)
