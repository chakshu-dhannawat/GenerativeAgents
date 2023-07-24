# This file conatins Memories class which stores the memories of the agent. It also contains the Reflection class which is used to retrieve the memories.

from GPT import GPT,getEmbedding
from Util import extractImportance,log
from Queries import *
from Params import *
import re
# from transformers import BertTokenizer, BertModel
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta

# Calendar class to keep track of the time
class Calendar:

  def __init__(self, day = "Tuesday February 13", time = "9:50 AM"):
    self.day = datetime.now().strftime("%A %B %d")
    self.time = time
    self.getDT()
    self.getString()

  def getDT(self):
    date = datetime.strptime(self.day, "%A %B %d")
    time = datetime.strptime(self.time, "%I:%M %p")
    self.dt = datetime.combine(date.date(), time.time())

  def getString(self):
    self.day = self.dt.strftime("%A %B %d")
    self.time = self.dt.strftime("%I:%M %p")

  def increment(self, seconds=1):
    self.dt += timedelta(seconds=seconds)
    self.getString()

  def incrementMins(self, mins=40):
    self.dt += timedelta(minutes=mins)
    self.getString()

  def nextDay(self):
    self.dt += timedelta(days=1)
    self.getString()

  def voting(self):
    self.dt = self.dt.replace(hour=8, minute=0)
    self.getString()

  def tasks(self):
    self.dt = self.dt.replace(hour=9, minute=50)
    self.getString()

  def night(self):
    self.dt = self.dt.replace(hour=21, minute=0)
    self.getString()

calendar = Calendar()

# Memory class to store the memories
class Memory():

  def __init__(self, observation=''):
    self.observation = observation
    self.creation = calendar.dt
    self.lastAccess = self.creation
    self.importance = 0
    self._id = ''
    # self.getImportance()

  def retrievalScore(self, query):
    return Alpha_Recency*self.getRecency() + Alpha_Importance*self.importance + Alpha_Relevance*self.getRelevancy(query)

  def getRecency(self, decay_factor = 0.99):
    time_difference = abs(calendar.dt - self.lastAccess)
    seconds_difference = time_difference.total_seconds()
    score = 10 * (decay_factor ** (seconds_difference / 3600))
    return max(0, min(score, 10))

  def getImportance(self):
    MAX_TRIES = 5
    while(self.importance==0 and MAX_TRIES>0):
      MAX_TRIES -= 1
      output = ""
      try:
        gpt = GPT()
        output = gpt.query(QUERY_IMPORTANCE.format(self.observation),name='QUERY_IMPORTANCE')
        self.importance = extractImportance(output)
      except:
        print(output)

  def getRelevancy(self, query):
    sentence_embedding = np.array(getEmbedding(self.observation))
    query_embedding = np.array(getEmbedding(query))
    similarity_score = cosine_similarity(sentence_embedding.reshape(1, -1), query_embedding.reshape(1, -1))
    relevance_score = similarity_score[0][0]
    # log(f"Relevancy - \n{query}\nMemory - \n{self.observation}\nRelevance Score- {relevance_score}")
    return 10*relevance_score

# Function to get the memory with the highest retrieval score
class Reflection(Memory):

  def __init__(self, observation, children=[]):
    super().__init__(observation)
    self.children = children