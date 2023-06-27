import Agent
from Util import *
from Queries import *
from Params import *
import random
import pygame
from pygame.locals import *
import os
import sys
import math
import cv2
import numpy as np
from Memories import calendar
import asyncio
from multiprocessing import Process


pygame.font.init()
pygame.init()
DEFAULT_IMAGE_SIZE = (WIN_WIDTH, WIN_HEIGHT)
speed = FPS*0.6


'''
====================
Assests
====================
'''

font = pygame.font.SysFont('comicsans', 30, True)
font2 = pygame.font.SysFont('consolas', 25, True)

bg = pygame.image.load(Path+'Town_background_new.png')

bgs = [pygame.image.load(Path+f'Background\\{i}.png') for i in range(100)]

# music = pygame.mixer.music.load(Path+'music.mp3')
# pygame.mixer.music.play(-1)


'''
====================
Warewolves Game
====================
'''

class Game:

  def __init__(self, agents):

    self.names = [agent.name for agent in agents]
    self.ids = {}
    for i,name in enumerate(self.names):
        self.ids[name] = i

    self.agents = agents

    self.n = len(agents)

    self.alive = [True]*self.n
    self.warewolf = [False]*self.n
    self.warewolf[0] = True

    # for agent in self.agents:
    #     agent.remember(agent.result)
    #     agent.reflect(2,2)

    self.w = WIN_WIDTH
    self.h = WIN_HEIGHT
    self.bg = pygame.transform.scale(bg, DEFAULT_IMAGE_SIZE)   
    self.bgs = bgs
    for i in range(100): 
      self.bgs[i] =  pygame.transform.scale(self.bgs[i], DEFAULT_IMAGE_SIZE)  
    self.changePhase = False 
    self.Night = 0
    self.bgId = -1
    self.win = pygame.display.set_mode((self.w,self.h))
    pygame.display.set_caption("Warewolves of Miller Hollow")
    self.clock = pygame.time.Clock()
    self.InitialPositions = InitialPositions
    
    self.reset()

  def getContext(self,name):
    context = ""
    sr = 0
    id = self.ids[name]
    for i,agent in enumerate(self.agents):
      if(not self.alive[i]): continue
      if(name==agent.name): continue
      sr += 1
      context = context + f"{sr}) {agent.name}: {self.agents[id].vote_context(agent.name)}\n"
    context = context[:-1]
    return context

  def getContextTownfolks(self,name):
    context = ""
    sr = 0
    id = self.ids[name]
    for i,agent in enumerate(self.agents):
      if(not self.alive[i]): continue
      if(self.warewolf[i]): continue
      sr += 1
      context = context + f"{sr}) {agent.name}: {self.agents[id].vote_context(agent.name)}\n"
    context = context[:-1]
    return context

  def nightVote(self):
    log("Currently it is Night, the Warewolves will kill a townfolk...\n")
    votes = [0]*self.n
    townfolks = []
    for i in range(self.n):
      if(self.alive[i] and not self.warewolf[i]):
        townfolks.append(i)
    for i in range(self.n):
      if(not self.warewolf[i]): continue
      context = self.getContextTownfolks(self.agents[i].name)
      vote = extractImportance(self.agents[i].brain.query(QUERY_NIGHT.format(self.agents[i].name,context))) - 1
      votes[townfolks[vote]]+=1
    kick = votes.index(max(votes))
    self.alive[kick] = 0
    self.kicked = self.names[kick]
    log(f"{self.kicked} has been killed by the Warewolves\n\n")

  def test(self):
    print(calendar.time)

  def dayVote(self):

    log("Currently it is Day, the Villagers will lynch someone...\n")

    context = []
    voters = []
    for i in range(self.n):
      if(self.alive[i]):
        voters.append(i)

    self.assembleTavern(voters)

    for i in range(self.n):
      if(not self.alive[i]): context.append("")
      else: context.append(self.getContext(self.agents[i].name))

    conversation = self.groupConversation(context,voters)

    votes = [0]*self.n
    log()
    for i,voteId in enumerate(voters):
      #print("Agent",i)
      #print(voteId)
      #print(context[voteId])
      names = ""
      j = 1
      for id in voters:
        if(id==voteId): continue
        names = names + f"{j}) {self.names[id]}\n"
        j += 1
      names = names[:-1]
      voteName = self.agents[voteId].brain.query(
         QUERY_DAY.format(self.agents[voteId].name,context[voteId],
                          conversation,self.agents[voteId].name,names))
      try:
        vote = self.names.index(voteName)
      except:
        voteName = self.findName(voteName)
        vote = self.names.index(voteName)
      log(f"{self.agents[voteId].name} voted to kick out {voteName}")
      votes[vote] += 1

    #print()
    # vote = extractImportance(agents[voteId].brain.query(QUERY_DAY.format(agents[voteId].name,context[voteId],conversation))) - 1
    #if(vote>=i): vote += 1
    # print(agents[voteId].name,"voted to kick out",self.names[voters[vote]])

    maxVotes = max(votes)
    if(votes.count(maxVotes)>1):
      log("\nNobody was lynched")
    else:
      kick = votes.index(maxVotes)
      self.alive[kick] = 0
      self.kicked = self.names[kick]
      log()
      log(f"{self.kicked} has been lynched by the Villagers")

    for agent in self.agents:
      agent.dest = None
      agent.location_name = 'Tavern'

  def findName(self,currName):
    for name in self.names:
      if name in currName:
        return name
    raise Exception(f"Invalid Name - {currName}")

  def groupConversation(self, context, voters):
      history = ""
      sakuraId = self.names.index("Sakura Kobayashi")
      if(sakuraId in voters): curr = sakuraId
      else: curr = random.choice(voters)
      reply = self.agents[curr].groupconv_init(self.kicked,context[curr])
      self.agents[curr].msg = reply 
      self.agents[curr].isSpeaking = True 
      self.draw_window()
      prev = curr
      moderator = GPT()
      names = ""
      for i,name in enumerate([self.agents[i].name for i in voters]):
        names = names + f"{i+1}) " + name + '\n'
      names = names[:-1]
      dialogues = 0
      lastFew = []
      while curr is not None:
          dialogues += 1
          log(reply)
          history = history + reply
          lastFew.append(reply)
          if(len(lastFew)>4): lastFew.pop(0)
          if(dialogues<MinDialogues): QUERY = QUERY_GROUPCONV_MODERATOR
          else: QUERY = QUERY_GROUPCONV_MODERATOR_END
          # currName = moderator.query(QUERY.format(history,names))
          currName = moderator.query(QUERY.format('\n'.join(lastFew[:2]),names))
          if("End Conversation" in currName): break
          try:
            curr = self.ids[currName]
          except:
            currName = self.findName(currName)
            curr = self.ids[currName]
          reply = self.agents[curr].groupconv(self.kicked, context[curr], '\n'.join(lastFew))
          # reply = self.agents[curr].groupconv(self.kicked, context[curr], history)
          self.agents[prev].isSpeaking = False 
          self.agents[curr].msg = reply 
          self.agents[curr].isSpeaking = True  
          self.draw_window()
          prev = curr
          history = history + '\n'
          for i in range(self.n):
            if(self.alive[i]): self.agents[i].remember(reply)
      self.agents[prev].isSpeaking = False 
      log("\nEnd of Conversation")
      return history
  

  def assembleTavern(self, voters):
    n = len(voters)
    for i in range(n):
      self.agents[voters[i]].dest = "Stop"
    angle = 2 * math.pi / n
    for i in range(n):
      theta = i * angle
      x = LOCATION_MAP['Tavern'][0] + int(TavernRadius * math.cos(theta))
      y = LOCATION_MAP['Tavern'][1] + int(TavernRadius * math.sin(theta))
      self.agents[voters[i]].tavern((x,y))
      # self.agents.dest = "Tavern"
     

  def switchPhase(self):
    self.changePhase = True

  def conversation(self, name1, name2):
    curr = 0
    agents = [self.agents[self.ids[name1]], self.agents[self.ids[name2]]]
    agents[0].talk_context(agents[1].name)
    agents[1].talk_context(agents[0].name)
    reply = agents[curr].talk_init(agents[1-curr].name, agents[1-curr].result)
    history = ""
    while reply is not None:
        log(reply)
        history = history + '\n' + reply
        curr = 1 - curr
        reply = agents[curr].talk(agents[1-curr].name, reply, history)
        history = history + '\n'
    log("\nEnd of Conversation")

  # def startNight(self):
     


  def reset(self) : 
      for agent in self.agents:
         agent.graphics_init(self.win)
      self.run = True

  def draw_time(self) :
      text = f"{calendar.day}\n{calendar.time}"
      position = (10,10)
      margin = 1

      text_lines = text.splitlines()  # Split the text into lines

      line_height = font2.get_linesize()
      y = position[1]

      for line in text_lines:
          text_surface = font2.render(line, True, BLACK)
          text_rect = text_surface.get_rect()
          text_rect.topleft = (position[0]+margin, y+margin)
          pygame.draw.rect(self.win, WHITE, (position[0], y, text_rect.width+2*margin, text_rect.height+2*margin))
          self.win.blit(text_surface, text_rect)
          y += line_height
      # text_surface = font2.render(text, True, BLACK)
      # text_rect = text_surface.get_rect()
      # pygame.draw.rect(self.win, WHITE, (0, 0, text_rect.width, text_rect.height))
      # self.win.blit(text_surface, text_rect)
  
  def draw_window(self) : 
      self.win.blit(self.bg,(0,0))
      for player in self.agents: 
          player.draw()      
      self.draw_time()
      pygame.display.update()

  def step(self) :

      for event in pygame.event.get() :

          if event.type == pygame.QUIT : 
              self.run = False
              pygame.quit()    
      
      keys = pygame.key.get_pressed()
      # self.agents[0].manual_move(keys)

      for player in self.agents:
          player.move() 
      
      if(self.changePhase):
        if(not self.Night):
          if(self.bgId==0):
              self.changePhase = False
              self.bgId=-1
              self.Night = True
          else:
              if(self.bgId==-1): self.bgId=100
              self.bgId-=1
              self.bg = self.bgs[self.bgId]
        else:
          if(self.bgId==99):
              self.changePhase = False
              self.bgId=-1
              self.Night = False
          else:
              self.bgId+=1
              self.bg = self.bgs[self.bgId]

      self.draw_window()
      calendar.increment(60/FPS)
      # test_process = Process(target=self.test)
      # test_process.start()
      #asyncio.run(self.test())
      #self.checkSpeakingProximity()
        
  def checkSpeakingProximity(self):
      for player1 in self.agents:
          for player2 in self.agents:
              if(player1!=player2):
                  if(abs(player1.x - player2.x) <100 and abs(player1.y - player2.y) < 100):
                      player1.isSpeaking = True
                      player2.isSpeaking = True
                      # player1.is_travelling = False
                      # player2.is_travelling = False
                      # endConversation = random.choice(['End', 'Continue'])
                      # if(endConversation=='End'):
                      #     player1.isSpeaking = False
                      #     player2.isSpeaking = False
                      #     player1.is_travelling = True
                      #     player2.is_travelling = True
                  else:
                      player1.isSpeaking = False
                      player2.isSpeaking = False
                      # player1.is_travelling = True
                      # player2.is_travelling = True
                  
                
   