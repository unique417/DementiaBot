#imports:
from transformers import AutoModelForCausalLM, AutoTokenizer,AutoModelWithLMHead
import torch
import json
from transformers import  Trainer, TrainingArguments
from generators.response_generator_base_class import ResponseGenerator
import requests



import os
import openai

#This line of code throws an error when missing the API key
openai.api_key = "*************************"


class Gpt3(ResponseGenerator):

    def __init__(self):
        #self.context = ""
        #print("self.comtext",self.context)
        self.conversation = "DementiaBot: Hello! My name is DementiaBot. My job is to help caregivers. I like to know you better, how are you?\nUser: Hello DementiaBot, I'm fine thank you. how are you?\nDementiaBot: I'm feeling fine! That's so sweet of you to ask. I know that being a human can sometimes be very challenging. How are you feeling? \nUser: I'm feeling a little overwhelmed. \nDementiaBot: I understand entirely. you have every right to feel this way. is there anything you like to do to make you feel better?\nUser: I like reading a good book, but I don't have the time.\nDementiaBot: It's so important to find time for things you enjoy! Maybe try reading a few pages before bed each night. Alternatively, you could try an audiobook so you can listen while you're doing other things.\n"

        #self.conversation = "DementiaBot: Hello! My name is DementiaBot. My job is to help caregivers. I like to know you better, how are you?\nUser: Hello DementiaBot, I am a caregiver. how are you?\nDementiaBot: I'm feeling fine! That's so sweet of you to ask. I know that being a caregiver can sometimes be very challenging. How are you feeling? \nUser: I'm feeling a little overwhelmed. \nDementiaBot: I understand entirely. you have every right to feel this way. is there anything you like to do to make you feel better?\nUser: I like reading a good book, but I don't have the time.\nDementiaBot: It's so important to find time for things you enjoy! Maybe try reading a few pages before bed each night. Alternatively, you could try an audiobook so you can listen while you're doing other things.\n"
        #self.userName= 'userName'
        #self.name= 'EVE'

    def name(self):
        return "Gpt3"


    def getLog(self, prompt):
        out = self.conversation + "\n"
        #out +='user:' , prompt,'EVE:'
        out += f'user: {prompt}\n DementiaBot: '
        self.conversation = out
        return out

    def getResponse(self, prompt): # Calls the api with all of the required parameters to generate a response

        response = openai.Completion.create(
          model="text-davinci-002",
          prompt=self.getLog(prompt),
          temperature=0.91,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

        for choice in response.choices:
            responseData = choice.text
        self.conversation += responseData + '\n'
        return responseData




    def response(self, prompt):
        response = self.getResponse(prompt)
        self.conversation += f'{prompt}\n {response}'
        return {'response': response}
