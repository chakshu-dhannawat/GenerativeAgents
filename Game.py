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
import multiprocessing
import time
import threading
from evaluation_metric import *
from gtts import gTTS
from translate import Translator


pygame.font.init()
pygame.init()
DEFAULT_IMAGE_SIZE = (WIN_WIDTH, WIN_HEIGHT)

speed = FPS*0.6

translator = Translator(to_lang='ja')


'''
====================
Assests
====================
'''

font = pygame.font.SysFont('comicsans', 30, True)
font2 = pygame.font.SysFont('consolas', 25, True)

bg = pygame.image.load(Path+'town.png')

bg_nodes = pygame.image.load(Path+'town_nodes_bg.jpg')
# bg2 = pygame.image.load(Path+'killing.gif')
# clock = pygame.time.Clock()
black_bg = pygame.image.load(Path+'blackbg.png')

night_pahse = pygame.image.load('Assets\\Phases\\Night_Phase.png')
day_phase = pygame.image.load('Assets\\Phases\\Day_Phase.png')
voting_phase = pygame.image.load('Assets\\Phases\\Voting Phase.png')
start_phase = pygame.image.load('Assets\\Phases\\START~2.png')

killframes = [pygame.image.load(Path+f'killing\\{i}.png') for i in range(N_Killing)]
farewellframesW = [pygame.image.load(Path+f'Farewell\\Warewolf\\{i}.png') for i in range(N_Farewell_W)]
farewellframesT = [pygame.image.load(Path+f'Farewell\\Townfolk\\{i}.png') for i in range(N_Farewell_T)]

bgs = [pygame.image.load(Path+f'Background\\{i}.png') for i in range(N_Background)]


# music = pygame.mixer.music.load(Path+'music.mp3')
# pygame.mixer.music.play(-1)


'''
====================
Fire 
====================
'''

fire_width = FIRE_SIZE[0]
fire_height = FIRE_SIZE[1]
fire_x = FIRE_CENTER[0]
fire_y = FIRE_CENTER[1]

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
    for i in range(self.n):
      if("warewolf" in self.agents[i].summary.split(';')[0]):
         self.warewolf[i] = True

    # for agent in self.agents:
    #     agent.remember(agent.result)
    #     agent.reflect(2,2)

    self.w = WIN_WIDTH
    self.h = WIN_HEIGHT
    self.bg = pygame.transform.scale(bg, DEFAULT_IMAGE_SIZE) 
    self.black_bg = pygame.transform.scale(black_bg, DEFAULT_IMAGE_SIZE)
    # self.bg2 = pygame.transform.scale(bg2, DEFAULT_IMAGE_SIZE) 
    self.bgs = bgs
    for i in range(N_Background): 
      self.bgs[i] =  pygame.transform.scale(self.bgs[i], DEFAULT_IMAGE_SIZE) 
    self.fire = True
    self.killing = False
    self.killId = 0
    self.elim = 0
    self.killframes = killframes
    for i in range(N_Killing): 
      self.killframes[i] =  pygame.transform.scale(self.killframes[i], DEFAULT_IMAGE_SIZE)  
    self.farewell = False
    self.farewellID = 0
    self.farewellframesT = farewellframesT
    self.farewellframesW = farewellframesW
    for i in range(N_Farewell_T): 
      self.farewellframesT[i] =  pygame.transform.scale(self.farewellframesT[i], DEFAULT_IMAGE_SIZE) 
    for i in range(N_Farewell_W): 
      self.farewellframesW[i] =  pygame.transform.scale(self.farewellframesW[i], DEFAULT_IMAGE_SIZE) 
    self.changePhase = False 
    self.Night = 0
    self.bgId = -1
    self.win = pygame.display.set_mode((self.w,self.h))
    pygame.display.set_caption("Warewolves of Miller Hollow")
    self.clock = pygame.time.Clock()
    self.InitialPositions = InitialPositions
    self.contexts = {}
    self.elimination = None
    self.elim = 0
    self.night_elimination = None
    self.day_phase = pygame.transform.scale(day_phase, DEFAULT_IMAGE_SIZE)
    self.night_phase = pygame.transform.scale(night_pahse, DEFAULT_IMAGE_SIZE)
    self.voting_phase = pygame.transform.scale(voting_phase, DEFAULT_IMAGE_SIZE)
    self.start_phase = pygame.transform.scale(start_phase, DEFAULT_IMAGE_SIZE)
    self.day_phase_show = False
    self.night_phase_show = False
    self.voting_phase_show = False
    self.start_phase_show = True

    self.reset()

  def getSingleContext(self,name1,name2):
      self.contexts[name1][name2] = self.agents[self.ids[name1]].vote_context(name2)
     
  def getContext(self,name,night=False):
    self.contexts[name] = {}
    threads = []
    for i in range(self.n):
        if(not self.alive[i]): continue
        if(name==self.names[i]): continue
        if(night and self.warewolf[i]): continue
        thread = threading.Thread(target=self.getSingleContext, args=(name, self.names[i],))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

  # def getContext(self,name,night=False):
  #   self.contexts[name] = {}
  #   for i in range(self.n):
  #       if(not self.alive[i]): continue
  #       if(name==self.names[i]): continue
  #       if(night and self.warewolf[i]): continue
  #       self.getSingleContext(name, self.names[i])


  # def getContext(self, name, night=False):
  #     self.contexts[name] = {}
  #     processes = []
  #     for i in range(self.n):
  #         if not self.alive[i]:
  #             continue
  #         if name == self.names[i]:
  #             continue
  #         if night and self.warewolf[i]:
  #             continue
  #         process = multiprocessing.Process(target=self.getSingleContext, args=(name, self.names[i]))
  #         process.start()
  #         processes.append(process)
  #     for process in processes:
  #         process.join()

  def speak(self,text):
    voicePath = "Assets\\voice.mp3"
    translation = translator.translate(text)
    tts = gTTS(translation, lang='ja')
    tts.save(voicePath)
    music = pygame.mixer.music.load(voicePath)
    pygame.mixer.music.play(1)
    while pygame.mixer.music.get_busy():
      time.sleep(0.1)
    pygame.mixer.music.unload()
  
  def nightVoteWarewolf(self,i,names):
    self.getContext(self.names[i],True)
    voteContext = ""
    sr = 1
    for key, value in self.contexts[self.names[i]].items():
        voteContext += f"{sr}) {key}: {value}\n"
        sr += 1
    voteName = self.agents[i].brain.query(QUERY_NIGHT.format(self.agents[i].name,voteContext,names))
    try:
      vote = self.names.index(voteName)
    except:
      voteName = self.findName(voteName)
      vote = self.names.index(voteName)
    if(self.warewolf[self.ids[voteName]]):
      vote = random.choice([index for index, value in enumerate(self.warewolf) if value is False and self.alive[index]])
    self.votes[vote] += 1

  def nightVote(self):

    self.night_phase_show = True

    log("Currently it is Night, the Warewolves will kill a townfolk...\n")
    self.votes = [0]*self.n

    names = ""
    j = 1
    for i in range(self.n):
      if(self.warewolf[i]): continue
      if(not self.alive[i]): continue
      names = names + f"{j}) {self.names[i]}\n"
      j += 1
    names = names[:-1]

    threads = []
    for i in range(self.n):
        if(not self.warewolf[i]): continue
        if(not self.alive[i]): continue
        thread = threading.Thread(target=self.nightVoteWarewolf, args=(i,names,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    kick = self.votes.index(max(self.votes))
    self.alive[kick] = 0
    self.kicked = self.names[kick]
    self.killing = True
    self.elimination = self.kicked
    log(f"{self.kicked} has been killed by the Warewolves\n\n")
    self.checkEnd()

  def dayVote(self):

    self.voting_phase_show = True

    log("Currently it is Day, the Villagers will lynch someone...\n")

    context = []
    voters = []
    for i in range(self.n):
      if(self.alive[i]):
        voters.append(i)

    self.assembleTavern(voters)

    threads = []
    for i in range(self.n):
        if(not self.alive[i]): continue
        thread = threading.Thread(target=self.getContext, args=(self.names[i],False,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    for i in range(self.n):
       if(not self.alive[i]): context.append("")
       else: 
          voteContext = ""
          sr = 1
          for key, value in self.contexts[self.names[i]].items():
              voteContext += f"{sr}) {key}: {value}\n"
              sr += 1
          context.append(voteContext[:-1])

    # votes = [0]*self.n
    # log()
    # for i,voteId in enumerate(voters):
    #   names = ""
    #   j = 1
    #   for id in voters:
    #     if(id==voteId): continue
    #     names = names + f"{j}) {self.names[id]}\n"
    #     j += 1
    #   names = names[:-1]
    #   voteName = self.agents[voteId].brain.query(
    #      QUERY_DAY_BEFORE.format(self.agents[voteId].name,context[voteId]
    #                              ,self.agents[voteId].name,names))
    #   try:
    #     vote = self.names.index(voteName)
    #   except:
    #     voteName = self.findName(voteName)
    #     vote = self.names.index(voteName)
    #   log(f"{self.agents[voteId].name} voted to kick out {voteName}")
    #   votes[vote] += 1

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
      self.farewell = True
      self.killing = True
      self.elimination = self.names[kick]
      log()
      log(f"{self.kicked} has been lynched by the Villagers")

    for agent in self.agents:
      agent.location_name = 'Tavern'
      agent.dest = None

    self.checkEnd()
      

  def findName(self,currName):
    for name in self.names:
      if name in currName or currName in name:
        return name
    for name in self.names:
      if name.split(' ')[0] in currName:
        return name
    raise Exception(f"Invalid Name - {currName}")

  def groupConversation(self, context, voters):
      history = ""
      
      remainingTownfolk = getDetails(self)
      remainingWarewolf = getDetails(self,True)

      curr = random.choice(voters)
      remaining = remainingWarewolf if self.warewolf[curr] else remainingTownfolk
      reply = self.agents[curr].groupconv_init(self.kicked,context[curr],remaining)

      try:
        replyMsg = extract_dialogue(reply)
      except: 
        replyMsg = reply

      thread = threading.Thread(target=self.speak, args=(replyMsg,))
      thread.start()
      self.agents[curr].msg = replyMsg 
      self.agents[curr].isSpeaking = True 
      # self.draw_window()
      prev = curr
      moderator = GPT()
      names = ""
      for i,name in enumerate([self.agents[i].name for i in voters]):
        names = names + f"{i+1}) " + name + '\n'
      names = names[:-1]
      dialogues = 0
      lastFew = []
      rating = 0 
      rating_n = 0
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
          remaining = remainingWarewolf if self.warewolf[curr] else remainingTownfolk
          reply = self.agents[curr].groupconv(self.kicked, context[curr], '\n'.join(lastFew), remaining)
          if(prev!=curr):
            rating += getResponseRating(lastFew[-1], reply, self.contexts[self.names[curr]][self.names[prev]], self.names[prev], self.names[curr])
            rating_n += 1
          thread.join()
          try:
            replyMsg = extract_dialogue(reply)
          except: 
            replyMsg = reply
          thread = threading.Thread(target=self.speak, args=(replyMsg,))
          thread.start()
          # reply = self.agents[curr].groupconv(self.kicked, context[curr], history)
          self.agents[prev].isSpeaking = False 
          self.agents[curr].msg = replyMsg 
          self.agents[curr].isSpeaking = True  
          # self.draw_window()
          prev = curr
          history = history + '\n'
          for i in range(self.n):
            if(self.alive[i]): self.agents[i].remember(reply)
      log("\nEnd of Conversation")
      if(rating_n==0): self.convRating = 0
      else: self.convRating = rating/rating_n 
      log(f"\nConversation Rating - {self.convRating}")
      # log(f"Turn Taking Ratio - {get_turn_taking_ratio(history)}")
      # log(f"Response Relevance - {calculate_response_relevance(history)}")
      # log(f"Agreement Metric - {calculate_agreement_metric(history)}")
      thread.join()
      self.agents[prev].isSpeaking = False 
      return history
  

  def assembleTavern(self, voters):
    n = len(voters)
    for i in range(n):
      self.agents[voters[i]].destination_path = []
      self.agents[voters[i]].dest = "Stop"
    angle = 2 * math.pi / n
    for i in range(n):
      theta = i * angle
      x = TavernCenter[0] + int(TavernRadius * math.cos(theta))
      y = TavernCenter[1] + int(TavernRadius * math.sin(theta))
      
      self.agents[voters[i]].tavern((x,y))

  def afternoon(self):
    self.day_phase_show = True
    self.generatePlanDay()
    while True:
      if(calendar.dt.hour in [1,13]): break
      if(calendar.dt.minute==0):
        now = calendar.time
        threads = []
        for i in range(self.n):
            if(not self.alive[i]): continue
            self.agents[i].task = None
            self.agents[i].taskReach = False
            thread = threading.Thread(target=self.agents[i].nextLocation, args=(now,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        self.observe(now)

        calendar.incrementMins(20)
      time.sleep(0.3)
      
    for i in range(self.n):
       self.agents[i].task = None 
       self.agents[i].taskReach = False  

  def observe(self,now=None):
    if(now is None): now = calendar.time
    for i in range(self.n):
        if(not self.alive[i]): continue
        for j in range(self.n):
          if(i==j or not self.alive[j]): continue
          if(self.agents[i].dest == self.agents[j].dest):
            if(self.agents[j].task is not None):
              self.agents[i].remember(f"{self.agents[i].name} saw {self.agents[j].name} {nodes[self.agents[j].task]} at {calendar.time}")     

  def generatePlanDay(self):
    threads = []
    for i in range(self.n):
        if(not self.alive[i]): continue
        thread = threading.Thread(target=self.agents[i].generatePlanDay)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

  def checkEnd(self):
    while(self.killing or self.elimination is not None):
      time.sleep(0.1)
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

  def stepKilling(self):
      if(self.fire): self.fire = False
      n = N_Killing
      if(self.farewell):
        if(self.warewolf[self.ids[self.kicked]]):
          n = N_Farewell_W 
        else: 
          n = N_Farewell_T
      if(self.killId==n*Speed_Killing):
          self.killing = False
          self.farewell = False
          self.killId = 0
          if(self.Night):
            self.bg = self.bgs[0]
          else:
            self.bg = self.bgs[N_Background-1] 
          self.fire = True
      else:
        if(self.farewell):
          if(self.warewolf[self.ids[self.kicked]]):
              self.bg = self.farewellframesW[self.killId//Speed_Killing]
          else:
              self.bg = self.farewellframesT[self.killId//Speed_Killing]
        else:
          self.bg = self.killframes[self.killId//Speed_Killing]
        self.killId+=1

  def stepPhase(self):
    if(not self.Night):
      if(self.bgId==0):
          self.changePhase = False
          self.bgId=-1
          self.Night = True
      else:
          if(self.bgId==-1): self.bgId=N_Background
          self.bgId-=1
          self.bg = self.bgs[self.bgId]
    else:
      if(self.bgId==N_Background-1):
          self.changePhase = False
          self.bgId=-1
          self.Night = False
      else:
          self.bgId+=1
          self.bg = self.bgs[self.bgId]

  def drawTaskEmoji(self):
    for i in range(self.n):
      if(not self.alive[i]): continue
      if self.agents[i].taskReach:
         self.agents[i].emoji_bubble('Cow')

  def drawElimination(self):

      if(self.elim==0):
        self.bg = self.black_bg
        self.win.blit(self.bg,(0,0))
        self.text1 = self.elimination + " has been Killed"
        if(self.warewolf[self.ids[self.elimination]]):
          self.text2 = self.elimination + " was a Warewolf"
        else: self.text2 = self.text2 = self.elimination + " was a Townfolk"
        self.elimination = self.agents[self.ids[self.elimination]]
        self.elimination.animationKillInit()
        self.elim = 1
        return 

      if(self.elimination.kill_x > WIN_WIDTH):
        self.elimination = None 
        self.elim = 0
        if(self.Night):
          self.bg = self.bgs[0]
        else:
          self.bg = self.bgs[99] 
        return
      
      text_surface = font2.render(self.text1, True, WHITE)
      text_rect = text_surface.get_rect()
      text_rect.centerx = WIN_WIDTH // 2
      text_rect.centery = WIN_HEIGHT // 4
      self.win.blit(text_surface,text_rect)

      text_surface = font2.render(self.text2, True, WHITE)
      text_rect = text_surface.get_rect()
      text_rect.centerx = WIN_WIDTH // 2
      text_rect.centery = 3*WIN_HEIGHT // 4
      self.win.blit(text_surface,text_rect)
      
      self.elimination.animationKillStep()

  
  def draw_window(self) : 
      # if(self.elimination):
      #   self.win.blit(self.bg2,(0,0))
      #   text = self.elimination + " has been lynched"
      #   text_surface = font.render(text,True,RED)
      #   self.win.blit(text_surface,(400,400))
      #   pygame.display.update()
      #   time.sleep(5)
      #   self.elimination = None
      # elif(self.night_elimination):
      #     self.win.blit(self.bg2,(0,0))
      #     text = self.night_elimination + " has been killed by the warewolves"
      #     text_surface = font.render(text,True,RED)
      #     self.win.blit(text_surface,(400,400))
      #     pygame.display.flip()
      #     time.sleep(5)
      #     self.night_elimination = None
      # else:
      self.win.blit(self.bg,(0,0))

      if(self.elimination is not None and not self.killing):
        self.drawElimination()

      if(not self.killing and self.elimination is None):

        for i,player in enumerate(self.agents): 
            if(self.alive[i]):
                player.draw() 
        self.draw_fire()  
        for i,player in enumerate(self.agents): 
            if(self.alive[i]):
                player.drawBubble() 

        self.drawTaskEmoji()  

        self.draw_time()

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

  def draw_phase(self):
      if(self.night_phase_show):
        self.win.blit(self.night_phase,(0,0))
        self.night_phase_show = False
      elif(self.day_phase_show):
        self.win.blit(self.day_phase,(0,0))
        self.day_phase_show = False
      elif(self.voting_phase_show):
        self.win.blit(self.voting_phase,(0,0))
        self.voting_phase_show = False
      elif(self.start_phase_show):
        self.win.blit(self.start_phase,(0,0))
        self.start_phase_show = False
      else:
         return
      pygame.display.update()
      time.sleep(2)

  def step(self) :

      for event in pygame.event.get() :

          if event.type == pygame.QUIT : 
              self.run = False
              pygame.quit()    
      
      keys = pygame.key.get_pressed()
      # self.agents[0].manual_move(keys)

      self.draw_phase()

      for i,player in enumerate(self.agents): 
          if(self.alive[i]):
              player.move() 
      
      if(self.changePhase):
        self.stepPhase()

      if(self.killing):
        self.stepKilling()

      self.draw_window()
      
      calendar.increment(60/FPS)

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
    
                  
                
   