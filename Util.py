from GPT import GPT
import re
from Graph import Graph,town
from Params import *
from Queries import QUERY_EVALUATION_METRICS

def log(text=''):
    print(text)
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

def getNames():
    people = ""
    for i in range(len(agentsDetails)):
      people = people + agentsDetails[i]['name'] + '; '
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
      ratings.append(float(line.split(' - ')[1]))
  average_rating = sum(ratings) / len(ratings)
  # log(f"Average Dialogue Rating: {average_rating}")
  return average_rating

def getDetails():
    details = ""
    cover = 'townfolk'
    for i,agent in enumerate(agentsDetails):
      if('warewolf' in agent['description']): cover = 'warewolf'
      else: cover = 'townfolk'
      details = details + f"{i+1}) {agent['name']}: {cover}\n"
    return details[:-1]

details = getDetails()

