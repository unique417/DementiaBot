#imports:
from transformers import AutoModelForCausalLM, AutoTokenizer,AutoModelWithLMHead
import torch
import json
from transformers import  Trainer, TrainingArguments
from generators.response_generator_base_class import ResponseGenerator
import os
import pandas as pd

device=('cuda' if torch.cuda.is_available() else 'cpu')
print('device',device)
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
conversation= os.getcwd()+'/generators/dementia.csv'
df = pd.read_csv(conversation)
question = df["Question"]
response = df["Response"]

data = []
for x in range(len(question)):
    q= '[YOU] : ' + question[x]
    r= '[BOT] : ' + response[x]
    data.append(q)
    data.append(r)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10)

trainer = Trainer(model=model,args=training_args,train_dataset=conversation)
model.to(device)
model.train()
model.state_dict()
#model.save_pretrained(path, saved_model=True)

class Dementia(ResponseGenerator):

    def __init__(self):
        pass

    def name(self):
        return "dementia"



    def generate_response(tokenizer, model, chat_round, chat_history_ids,text):
        new_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt').to(device)
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_round > 0 else new_input_ids
        chat_history_ids = model.generate(bot_input_ids, max_length=1250, pad_token_id=tokenizer.eos_token_id)
        #[print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
        response=tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return chat_history_ids, response

    def response(self,text):
         chat_history_ids = None
         for chat_round in range(1):
             chat_history_ids,response = Dementia.generate_response(tokenizer, model, chat_round, chat_history_ids,text)
             return {'response': response}
