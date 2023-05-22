class Yes_no:
    def __init__(self):
        pass

    def classifier(self,text):

        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        for ele in text:
            if ele in punc:
                text = text.replace(ele, "")

        y = ["yeah","yes","yup","yeah","yea","ye","ya","yes","yas","right","yess","True","yee","yeet","ofcourse","definitely","absolutly", "I think so","I believe so"]
        n = ["no","No","nope","naw","nae","noo","na","maybe","not really","False","nah", "I don't think so", "not", "not at all", "None"]

        for i in y:
            if i in text.lower():
                x="yes"
                return x

        for j in n:
            if j in text:
                x="no"
                return x

        return None
