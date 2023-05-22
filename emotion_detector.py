from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")

model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")
class Emotion():


    def __init__(self):
        pass
    def get_emotion(self,text):
      input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')

      output = model.generate(input_ids=input_ids,
                   max_length=2)

      dec = [tokenizer.decode(ids) for ids in output]
      label = dec[0]
      return label
