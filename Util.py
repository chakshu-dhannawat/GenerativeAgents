# This file contains functions related to Plan Extraction, Plan Execution, and Plan Evaluation, Memory Retrieval, and Dialogue Generation.
# [このファイルには、プラン抽出、プラン実行、プラン評価、メモリ検索、ダイアログ生成に関する関数が含まれています。]

from GPT import GPT
import re
from Graph import Graph,town
from Params import *
from Queries import QUERY_EVALUATION_METRICS
from threading import Lock
import os
import pygame
import random
import textwrap

lock = Lock()

def log(text=''):
    print(text)
    with lock:
      with open("logs.txt", "a") as file:
          file.write(text + "\n")

def extractImportance(output):
    numbers = re.findall(r'\d+', output)
    if numbers:
        lowest_number = min(map(int, numbers))
        return lowest_number
    else:
        return 0

def extractPlan(hourly):
    plan = {}
    sep = '\n\n'
    if(hourly.count('\n\n')<4): sep = '\n'
    h = hourly.split(sep)
    if(not h[0][0].isdigit()):
      h = h[1:]
    if(not h[-1][0].isdigit()):
      h = h[:-1]

    for p in h:
      try:
        k,v = p.split(': ')
        plan[k] = v
      except:
        pass

    return shuffle_plan(plan)

def getNextDay(today):
    gpt = GPT()
    tomm = gpt.query("Today is Wednesday February 13, tomorrow is")
    return tomm[:-1]

def timeKey(time_string):
    time_parts = time_string.split(":")
    hours = int(time_parts[0])
    rest = time_parts[1]
    return f"{hours}:{rest}"

def printPlan(plan,name,day):
    planString = f"{name}'s Plan for {day} -\n\n"
    for key in plan.keys():
       planString += f"{key} : {plan[key]}\n"
    planString += '\n.....................\n\n'
    log(planString)

def getHubs():
    areas = ""
    for i,node in enumerate(hubs):
      areas = areas + f"{i+1}) " + node + " - " + nodes[node] + '\n'
    return areas

def shuffle_plan(dictionary):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    random.shuffle(values)
    shuffled_dict = {k: v for k, v in zip(keys, values)}
    return shuffled_dict

def getTasks(hub,game,werewolf=False):
    tasks = ""
    if(werewolf):
      tasksList = [node for node in nodes if "task" in node and hub in node]
    else:
      tasksList = [node for node in nodes if "task" in node and hub in node and "Sabotage" not in TASK_EMOJI_MAP[node]] 
    for i,node in enumerate(tasksList):
      tasks = tasks + f"{i+1}) " + node + " - " + nodes[node] + '\n'
    return tasks,tasksList
  
def getAllTasks(werewolf=False):
    tasks = ""
    if(werewolf):
      tasksList = [node for node in nodes if "task" in node]
    else:
      tasksList = [node for node in nodes if "task" in node and "Sabotage" not in TASK_EMOJI_MAP[node]]
    for i,node in enumerate(tasksList):
      tasks = tasks + f"{i+1}) " + node + " - " + nodes[node] + '\n'
    return tasks,tasksList

def getPeople():
    people = ""
    for i in range(len(agentsDetails)):
      people = people + agentsDetails[i]['name'] + " - " + agentsDetails[i]['description'] + '; '
    return people

def getMemories(stream, n=100):
    #TODO: Retrieve using timestamp
    if(len(stream)>n): stream = stream[-n:]
    memories = ""
    i = 1
    for mem in stream:
      memories = memories + f"{i}) " + mem.observation + "\n"
      i += 1
    return memories

def extractHub(output):
    for node in hubs:
      if(node in output): return node 
    return "Tavern"

def extractQuestions(output):
    questions = []
    sep = '\n\n'
    if(output.count('\n\n')<4): sep = '\n'
    Q = output.split(sep)
    if(Q[0]=='' or not Q[0][0].isdigit()):
      Q = Q[1:]
    if(Q[-1]=='' or not Q[-1][0].isdigit()):
      Q = Q[:-1]

    s = 3
    for i,q in enumerate(Q):
      try:
        if((i+1)%10==0): s+=1
        Q[i] = q[s:]
      except:
        pass

    return Q

def getRetrievedMemories(stream):
    memories = ""
    i = 1
    for mem in stream:
      memories = memories + f"{i}) " + mem + "\n"
      i += 1
    return memories

def getResponseRating(dialogue, response, context, agent1, agent2):
  gpt = GPT()
  rating = gpt.query(QUERY_EVALUATION_METRICS.format(agent2, agent2, agent1, context,agent1, dialogue, agent2, response),name='QUERY_EVALUATION_METRICS')
  lines = rating.split('\n')
  ratings = []
  for line in lines:
      try:
        ratings.append(float(line.split('-')[1].strip()))
      except:
        pass
  average_rating = sum(ratings) / len(ratings)
  return average_rating

def extract_dialogue(dialogue):
    dialogue = dialogue.split(':')[1].strip()
    if(dialogue[0] in ['\'','"']):
      dialogue = dialogue[1:-1]
    return dialogue.split('(')[0]

def getDetails(game,includeCover=False):
    details = ""
    cover = 'townfolk'
    sr = 0
    for i in range(game.n):
      if(not game.alive[i]): continue
      sr += 1
      if(not includeCover):
         details = details + f"{sr}) {game.names[i]}\n"
         continue
      if(game.werewolf[i]): cover = 'werewolf'
      else: cover = 'townfolk'
      details = details + f"{sr}) {game.names[i]}: {cover}\n"
    return details[:-1]

def getNames(game,townfolks=True):
    details = ""
    sr = 0
    for i in range(game.n):
      if(not game.alive[i]): continue
      if(townfolks and not game.werewolf[i]):
        sr += 1
        details = details + f"{sr}) {game.names[i]}\n"
      if(not townfolks and game.werewolf[i]):
        sr += 1
        details = details + f"{sr}) {game.names[i]}\n"
    return details[:-1]   

def getAllDetails():
    details = ""
    cover = 'townfolk'
    for i,agent in enumerate(agentsDetails):
      if('werewolf' in agent['description']): cover = 'werewolf'
      else: cover = 'townfolk'
      details = details + f"{i+1}) {agent['name']}: {cover}\n"
    return details[:-1]

def outline_character(image):
  border_width = 2
  image = image.convert_alpha()
  width, height = image.get_size()
  outline_image = pygame.Surface((width, height), pygame.SRCALPHA)
  
  for x in range(width):
      for y in range(height):
          color = image.get_at((x, y))
          if color.a > 0:
              if (
                  get_alpha(image, x - 1, y) == 0
                  or get_alpha(image, x + 1, y) == 0
                  or get_alpha(image, x, y - 1) == 0
                  or get_alpha(image, x, y + 1) == 0
              ):
                  color = RED

          outline_image.set_at((x, y), color)

  bordered_image = outline_image.copy()

  for x in range(width):
      for y in range(height):
          color = outline_image.get_at((x, y))

          if color == RED:
              for i in range(border_width):
                  if (
                      x - i >= 0
                      and y - i >= 0
                      and x + i < width
                      and y + i < height
                  ):
                      bordered_image.set_at((x - i, y - i), RED)
                      bordered_image.set_at((x + i, y - i), RED)
                      bordered_image.set_at((x - i, y + i), RED)
                      bordered_image.set_at((x + i, y + i), RED)

  return bordered_image


def get_alpha(image, x, y):
    width, height = image.get_size()
    if 0 <= x < width and 0 <= y < height:
        return image.get_at((x, y)).a
    return 0
  
  
  
def split_text_into_lines(text):
    lines = textwrap.wrap(text, width=6)
    return "\n".join(lines)



details = getAllDetails()