import os
import openai
import json
from datetime import datetime, timedelta
import pymongo
from pymongo import MongoClient
import re
import random
from threading import Lock
from dotenv import load_dotenv
import os
import time
from fpdf import FPDF
from Params import PDF_Name

load_dotenv()
lock = Lock()

def addUsage(tokens):
  with lock:
    f = open('usage.json')
    usage = json.load(f) + tokens
    with open('usage.json', 'w') as f:
      json.dump(usage, f)

# with open('usage.json', 'w') as f:
#     json.dump(0, f)

openai.api_type = os.getenv('OpenAI_Type')

openai.api_base = os.getenv('OpenAI_Base')

openai.api_version = os.getenv('OpenAI_Version')

openai.api_key = os.getenv("OpenAI_API_KEY")


class GPT:


  def __init__(self,context="You are an assistant giving to the point answers. Just tell the answers instead of forming whole sentences"):

    self.context = context
    self.messages = [{"role": "system", "content": context}]


  def query(self,qry,remember=True,tries=0,input_ts=None,name=''):

    self.messages.append({"role":"user", "content":qry})
    if(input_ts is None):
      input_ts = time.time()

    try:
      response = openai.ChatCompletion.create(
          engine="gpt-35-turbo",
          messages = self.messages,
          temperature=0.7,
          max_tokens=1000,
          request_timeout=10+10*tries,
          top_p=0.95,
          frequency_penalty=0,
          presence_penalty=0,
          stop=None)
    except: 
      if(tries>3):
        raise Exception(f"Query Timeout - {qry}")
      return self.query(qry,remember,tries+1,input_ts)

    try:
      answer = response["choices"][0]["message"]["content"]
    except:
      if(tries>2):
        print(qry)
        raise Exception("Error in Query Response")
      return self.query(qry,remember,tries+1,input_ts)
    
    self.log(qry,answer,input_ts,time.time(),response["usage"]["total_tokens"],name)

    if(remember):
      self.messages.append({"role":"assistant", "content":answer})
    else:
      self.messages.pop()

    addUsage(response["usage"]["total_tokens"])

    return answer
  
  def log(self, input, output, input_ts, output_ts, tokens, name):
    text = f'=====================================================\n{name}\n=====================================================\nResponse Time : {round(output_ts-input_ts,2)} s\nTokens Used : {tokens}\n\n------------\nQUERY [{time.strftime("%H:%M:%S", time.localtime(input_ts))}]\n------------\n{input}\n\n------------\nOUTPUT [{time.strftime("%H:%M:%S", time.localtime(output_ts))}]\n------------\n{output}\n\n\n\n'
    with lock:
      with open("Logs\\logs.txt", "a") as file:
          file.write(text)
      pdf = FPDF()
      pdf.add_page()
      pdf.set_font("Times", size=12)
      with open("Logs\\logs.txt", "r") as file:
          text = file.read()
      pdf.multi_cell(0, 10, text.encode('utf-8').decode('latin-1'))
      pdf.output(PDF_Name)


  def reset(self):

    self.messages = [{"role": "system", "content": self.context}]