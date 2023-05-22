#imports:
from transformers import AutoModelForCausalLM, AutoTokenizer,AutoModelWithLMHead
import torch
import json
from transformers import  Trainer, TrainingArguments
from generators.response_generator_base_class import ResponseGenerator
import os

device=('cuda' if torch.cuda.is_available() else 'cpu')
print('device',device)
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
conversation= os.getcwd()+'/generators/dialogpt.json'
with open(conversation, 'r') as f:
    df =json.load(f)
data = []
for x in df:
    for y in range(len(x['dialog'])-1):
      answer = '[BOT] : ' + x['dialog'][y+1]['text']
      question = '[YOU] : ' + x['dialog'][y]['text']
      data.append(question)
      data.append(answer)

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

class DialoGPResponseGenerator(ResponseGenerator):

    def __init__(self):
        pass

    def name(self):
        return "DialoGPT"



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
             chat_history_ids,response = DialoGPResponseGenerator.generate_response(tokenizer, model, chat_round, chat_history_ids,text)
             return {'response': response}
