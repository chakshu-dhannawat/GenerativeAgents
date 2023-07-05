from GPT import GPT
import re
from Graph import Graph,town
from Params import *
from Queries import QUERY_EVALUATION_METRICS
from threading import Lock
import os
import pygame

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

    return plan

def getNextDay(today):
    gpt = GPT()
    tomm = gpt.query("Today is Wednesday February 13, tomorrow is")
    return tomm[:-1]

def printPlan(plan):
    # items = re.split(r'\d+\)', plan)
    # items = [item.strip() for item in items if item.strip()]
    # for i,item in enumerate(items):
    #   log(f"{i+1})",item)
    for key in plan.keys():
       log(f"{key} : {plan[key]}")

def getHubs():
    areas = ""
    for i,node in enumerate(hubs):
      areas = areas + f"{i+1}) " + node + " - " + nodes[node] + '\n'
    return areas

def getTasks(hub):
    tasks = ""
    tasksList = [node for node in nodes if "task" in node and hub in node]
    for i,node in enumerate(tasksList):
      tasks = tasks + f"{i+1}) " + node + " - " + nodes[node] + '\n'
    return tasks,tasksList

def getPeople():
    people = ""
    for i in range(len(agentsDetails)):
      people = people + agentsDetails[i]['name'] + " - " + agentsDetails[i]['description'] + '; '
    return people

# def getNames():
#     people = ""
#     for i in range(len(agentsDetails)):
#       people = people + agentsDetails[i]['name'] + '; '
#     return people

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
    # try:
    #   a = nodes[output]
    #   return output
    # except:
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
  rating = gpt.query(QUERY_EVALUATION_METRICS.format(agent2, agent2, agent1, context,agent1, dialogue, agent2, response))
  # log(f"Dialogue Rating:\n{rating}")
  lines = rating.split('\n')
  ratings = []
  for line in lines:
      try:
        ratings.append(float(line.split('-')[1].strip()))
      except:
        pass
  average_rating = sum(ratings) / len(ratings)
  # log(f"Average Dialogue Rating: {average_rating}")
  return average_rating

def extract_dialogue(dialogue):
    # dialogue = re.search(': "(.*?)"', string)
    # if dialogue:
    #     return dialogue.group(1)
    # elif(re.search(':"(.*?)"', string)):
    #     return re.search(':"(.*?)"', string).group(1)
    # elif(re.search(": '(.*?)'", string)):
    #     return re.search(": '(.*?)'", string).group(1)
    # elif(re.search(":'(.*?)'", string)):
    #     return re.search(":'(.*?)'", string).group(1)
    # elif(re.search(":(.*?)", string)):
    #     return re.search(":(.*?)", string).group(1)
    # elif(re.search(": (.*?)", string)):
    #     return re.search(": (.*?)", string).group(1)
    # return None

    dialogue = dialogue.split(':')[1].strip()
    if(dialogue[0] in ['\'','"']):
      dialogue = dialogue[1:-1]
    return dialogue

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
      if(game.warewolf[i]): cover = 'warewolf'
      else: cover = 'townfolk'
      details = details + f"{sr}) {game.names[i]}: {cover}\n"
    return details[:-1]

def getNames(game,townfolks=True):
    details = ""
    sr = 0
    for i in range(game.n):
      if(not game.alive[i]): continue
      if(townfolks and not game.warewolf[i]):
        sr += 1
        details = details + f"{sr}) {game.names[i]}\n"
      if(not townfolks and game.warewolf[i]):
        sr += 1
        details = details + f"{sr}) {game.names[i]}\n"
    return details[:-1]   

def getAllDetails():
    details = ""
    cover = 'townfolk'
    for i,agent in enumerate(agentsDetails):
      if('warewolf' in agent['description']): cover = 'warewolf'
      else: cover = 'townfolk'
      details = details + f"{i+1}) {agent['name']}: {cover}\n"
    return details[:-1]
    
def outline_character(image):
    # Convert the image to a surface with per-pixel alpha
    image = image.convert_alpha()
    # Get the width and height of the image
    width, height = image.get_size()
    # Create a blank surface with per-pixel alpha
    outline_image = pygame.Surface((width, height), pygame.SRCALPHA)
    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the color of the current pixel
            color = image.get_at((x, y))
            # Check if the pixel is fully opaque
            if color.a > 0:
                # Check if any of the neighboring pixels are transparent
                if (
                    get_alpha(image, x - 1, y) == 0
                    or get_alpha(image, x + 1, y) == 0
                    or get_alpha(image, x, y - 1) == 0
                    or get_alpha(image, x, y + 1) == 0
                ):
                    # Set the color of the current pixel to red
                    color = (255, 0, 0, 255)
            # Set the color of the current pixel on the outline image
            outline_image.set_at((x, y), color)
    return outline_image

def get_alpha(image, x, y):
    width, height = image.get_size()
    if 0 <= x < width and 0 <= y < height:
        return image.get_at((x, y)).a
    return 0


details = getAllDetails()