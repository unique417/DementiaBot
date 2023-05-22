from openie import StanfordOpenIE

class StanfordOpenIEWrapper:
    def __init__(self):
        self.client = StanfordOpenIE()

    def extract_triples(self, text):
        triples = self.client.annotate(text)
        return [[t['subject'], t['relation'], t['object']] for t in triples]



if __name__=='__main__':
    model = StanfordOpenIEWrapper()
    print(model.extract_triples('The quick brown fox jumped over the lazy dog. It was quite a sight to see.'))
