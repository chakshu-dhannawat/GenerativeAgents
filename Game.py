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
import time
import threading


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
Fire 
====================
'''

fire_width = 50
fire_height = 50
fire_x = 810
fire_y = 545

fire_particles = []

for _ in range(100):
    x = random.randint(fire_x, fire_x + fire_width)
    y = random.randint(fire_y, fire_y + fire_height//2)
    dx = random.uniform(-0.1, 0.1)
    dy = random.uniform(-0.2, -0.1)
    size = random.uniform(0.5,1.5)
    fire_particles.append((x, y, dx, dy, size))

fire_animation_frames = [pygame.image.load(f'Assets\\Fire\\{i}.png') for i in range(40)]
fire_animation_frames.extend(fire_animation_frames[::-1])

current_frame = 0
frame_count = 0
animation_speed = 4  


'''
====================
Emojis
====================
'''

# Load and scale the emoji images
#eat_emoji = pygame.transform.scale(pygame.image.load(Path + "Eat_emoji.png"), EMOJI_SIZE)
assistant_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "assistant.png"), EMOJI_SIZE)
broom_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "broom.png"), EMOJI_SIZE)
bucket_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "bucket.png"), EMOJI_SIZE)
bulb_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "bulb.png"), EMOJI_SIZE)
cook_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "cook.png"), EMOJI_SIZE)
cow_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "cow.png"), EMOJI_SIZE)
eggs_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "eggs.png"), EMOJI_SIZE)
electricRepair_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "electricRepair.png"), EMOJI_SIZE)
fish_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "fish.png"), EMOJI_SIZE)
fishingPole_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "fishingPole.png"), EMOJI_SIZE)
houseMechanic_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "houseMechanic.png"), EMOJI_SIZE)
houses_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "houses.png"), EMOJI_SIZE)
lamp_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "lamp.png"), EMOJI_SIZE)
pick_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "pick.png"), EMOJI_SIZE)
prayer_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "prayer.png"), EMOJI_SIZE)
shrine_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "shrine.png"), EMOJI_SIZE)
wellMechanic_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "wellMechanic.png"), EMOJI_SIZE)
wood_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "wood.png"), EMOJI_SIZE)

# Create a dictionary of emojis
EMOJI = {
            #'Eat': eat_emoji,
            'Assistant': assistant_emoji,
            'Broom': broom_emoji,
            'Bucket': bucket_emoji,
            'Bulb': bulb_emoji,
            'Cook': cook_emoji,
            'Cow': cow_emoji,
            'Eggs': eggs_emoji,
            'Electric Repair': electricRepair_emoji,
            'Fish': fish_emoji,
            'Fishing Pole': fishingPole_emoji,
            'House Mechanic': houseMechanic_emoji,
            'Houses': houses_emoji,
            'Lamp': lamp_emoji,
            'Pick': pick_emoji,
            'Prayer': prayer_emoji,
            'Shrine': shrine_emoji,
            'Well Mechanic': wellMechanic_emoji,
            'Wood': wood_emoji
        }



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
    self.contexts = {}
    
    self.reset()

  def getContext(self,name):
    self.contexts[name] = {}
    context = ""
    sr = 0
    id = self.ids[name]
    for i,agent in enumerate(self.agents):
      if(not self.alive[i]): continue
      if(name==agent.name): continue
      sr += 1
      voteContext = self.agents[id].vote_context(agent.name)
      self.contexts[name][agent.name] = voteContext
      context = context + f"{sr}) {agent.name}: {voteContext}\n"
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
    self.checkEnd()


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
      agent.location_name = 'Tavern'
      agent.dest = None

    self.checkEnd()
      

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
          getResponseRating(lastFew[-1], reply, self.contexts[self.names[curr]][self.names[prev]], self.names[prev], self.names[curr])
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
      x = TavernCenter[0] + int(TavernRadius * math.cos(theta))
      y = TavernCenter[1] + int(TavernRadius * math.sin(theta))
      self.agents[voters[i]].tavern((x,y))

  def afternoon(self):
    self.generatePlanDay()
    while True:
      if(calendar.dt.minute==0):
        now = calendar.time
        threads = []
        for i in range(self.n):
            if(not self.alive[i]): continue
            thread = threading.Thread(target=self.agents[i].nextLocation, args=(now,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        # for i in range(self.n):
        #   if(self.alive[i]):
        #      self.agents[i].nextLocation()
        time.sleep(5)  

  def generatePlanDay(self):
    for i in range(self.n):
      if(self.alive[i]):
         self.agents[i].generatePlanDay()

  def checkEnd(self):
    players = [0,0]
    for i in range(self.n):
       if(self.alive[i]):
          players[self.warewolf[i]]+=1
    if(players[1]==0):
      self.run = False
      log('\n=== TOWNFOLKS WIN ===')
      pygame.quit()
    if(players[1]>=players[0]):
      self.run = False 
      log('\n=== WAREWOLVES WIN ===')
      pygame.quit()
          
    
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
      for i,player in enumerate(self.agents): 
          if(self.alive[i]):
              player.draw()      
      self.draw_time()
      self.draw_fire()
      pygame.display.update()

  def draw_fire(self):
    global current_frame, frame_count, animation_speed
    # Update fire particles
    for i in range(len(fire_particles)):
        x, y, dx, dy, size = fire_particles[i]
        x += dx
        y += dy
        size -= 0.01
        if size <= 0:
            fire_particles[i] = (random.randint(fire_x, fire_x + fire_width),
                                 random.randint(fire_y, fire_y + fire_height//2),
                                 random.uniform(-0.1, 0.1),
                                 random.uniform(-0.2, -0.1),
                                 random.uniform(0.5,1.5))
        else:
            fire_particles[i] = (x, y, dx, dy, size)

    # Draw central fire
    fire_image = pygame.transform.scale(fire_animation_frames[current_frame], (fire_width, fire_height))
    self.win.blit(fire_image, (fire_x, fire_y))

    # Update fire animation frames
    frame_count += 1
    if frame_count >= animation_speed:
        current_frame = (current_frame + 1) % len(fire_animation_frames)
        frame_count = 0

    # Draw fire particles
    for x, y, _, _, size in fire_particles:
        if size > 0:
            pygame.draw.circle(self.win, YELLOW, (int(x), int(y)), int(size))

  def step(self) :

      for event in pygame.event.get() :

          if event.type == pygame.QUIT : 
              self.run = False
              pygame.quit()    
      
      keys = pygame.key.get_pressed()
      # self.agents[0].manual_move(keys)

      for i,player in enumerate(self.agents): 
          if(self.alive[i]):
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
    
                  
                
   