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
import pyautogui
from HoveringBox import HoverTextBox


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
font3 = pygame.font.Font(None, 40)

bg = pygame.image.load(Path+'town.png')

bg_nodes = pygame.image.load(Path+'town_nodes_bg.jpg')
# bg2 = pygame.image.load(Path+'killing.gif')
# clock = pygame.time.Clock()
black_bg = pygame.image.load(Path+'blackbg.png')

night_pahse = pygame.image.load('Assets\\Phases\\Night_Phase.png')
day_phase = pygame.image.load('Assets\\Phases\\Day_Phase.png')
voting_phase = pygame.image.load('Assets\\Phases\\Voting Phase.png')
start_phase = pygame.image.load('Assets\\Phases\\START~2.png')
game_end = pygame.image.load('Assets\\Phases\\Game_End.png')
warewolves_win = pygame.image.load('Assets\\Phases\\Warewolves_Win.png')
townfolks_win = pygame.image.load('Assets\\Phases\\Townfolks_Win.png')

night_phase_japanese = pygame.image.load('Assets\\Phases\\Night_Phase_Japanese.png')
day_phase_japanese = pygame.image.load('Assets\\Phases\\Day_Phase_Japanese.png')
voting_phase_japanese = pygame.image.load('Assets\\Phases\\Voting_Phase_Japanese.png')
townfolks_win_japanese = pygame.image.load('Assets\\Phases\\Townfolks_Win_Japanese.png')
warewolves_win_japanese = pygame.image.load('Assets\\Phases\\Warewolves_Win_Japanese.png')

killframes = [pygame.image.load(Path+f'killing\\{i}.png') for i in range(N_Killing)]
farewellframesW = [pygame.image.load(Path+f'Farewell\\Warewolf\\{i}.png') for i in range(N_Farewell_W)]
farewellframesT = [pygame.image.load(Path+f'Farewell\\Townfolk\\{i}.png') for i in range(N_Farewell_T)]

bgs = [pygame.image.load(Path+f'Background\\{i}.png') for i in range(N_Background)]


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
sabotage_emoji = pygame.transform.scale(pygame.image.load(Emoji_Path + "sabotage.png"), EMOJI_SIZE)

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
            'Wood': wood_emoji,
            'Sabotage': sabotage_emoji
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
    self.fps = FPS
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
    self.VelFactor = 1
    self.win = pygame.display.set_mode((self.w,self.h),RESIZABLE)
    pygame.display.set_caption("Warewolves of Miller Hollow")
    self.clock = pygame.time.Clock()
    self.InitialPositions = InitialPositions
    self.contexts = {}
    for i in range(self.n):
      self.contexts[self.names[i]] = {}
    self.elimination = None
    self.elim = 0
    self.night_elimination = None
    self.day_phase = pygame.transform.scale(day_phase, DEFAULT_IMAGE_SIZE)
    self.day_phase_japanese = pygame.transform.scale(day_phase_japanese, DEFAULT_IMAGE_SIZE)
    self.night_phase = pygame.transform.scale(night_pahse, DEFAULT_IMAGE_SIZE)
    self.night_phase_japanese = pygame.transform.scale(night_phase_japanese, DEFAULT_IMAGE_SIZE)
    self.voting_phase = pygame.transform.scale(voting_phase, DEFAULT_IMAGE_SIZE)
    self.voting_phase_japanese = pygame.transform.scale(voting_phase_japanese, DEFAULT_IMAGE_SIZE)
    self.townfolks_win = pygame.transform.scale(townfolks_win, DEFAULT_IMAGE_SIZE)
    self.townfolks_win_japanese = pygame.transform.scale(townfolks_win_japanese, DEFAULT_IMAGE_SIZE)
    self.warewolves_win = pygame.transform.scale(warewolves_win, DEFAULT_IMAGE_SIZE)
    self.warewolves_win_japanese = pygame.transform.scale(warewolves_win_japanese, DEFAULT_IMAGE_SIZE)
    self.start_phase = pygame.transform.scale(start_phase, DEFAULT_IMAGE_SIZE)
    self.end_phase = pygame.transform.scale(game_end, DEFAULT_IMAGE_SIZE)
    self.day_phase_show = False
    self.day_phase_japanese_show = False
    self.night_phase_show = False
    self.night_phase_japanese_show = False
    self.voting_phase_show = False
    self.voting_phase_japanese_show = False
    self.townfolks_win_show = False
    self.townfolks_win_japanese_show = False
    self.warewolves_win_show = False
    self.warewolves_win_japanese_show = False
    self.start_phase_show = True
    self.end_phase_show = False
    self.nobodyLynch = False
    self.convs = 0
    self.ClockPrev = Clock_Speed
    # self.taskOccupied = {hub:[False]*(len([node for node in nodes.keys() if "task" in node and hub in node])) for hub in hubs}
    self.HoverBox_agents = {}
    self.reset()

    self.playBgMusic()  

    pyautogui.click(500, 500, button='left')
    time.sleep(0.01)
    pyautogui.moveTo(pyautogui.size()[0]-1,0)


  def getSingleContext(self,name1,name2):
      self.contexts[name1][name2] = self.agents[self.ids[name1]].vote_context(name2)
     
  def getContext(self,name,night=False):
    # self.contexts[name] = {}
    threads = []
    for i in range(self.n):
        if(not self.alive[i]): continue
        if(name==self.names[i]): continue
        #if(night and self.warewolf[i]): continue
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

  def speak(self,text,curr):
    voicePath = "Assets\\voice.mp3"
    translation = translator.translate(text)
    tts = gTTS(translation, lang='ja')
    tts.save(voicePath)
    self.agents[curr].isSpeaking = True
    music = pygame.mixer.music.load(voicePath)
    pygame.mixer.music.play(1)
    while pygame.mixer.music.get_busy():
      time.sleep(0.1)
    pygame.mixer.music.unload()
    self.agents[curr].isSpeaking = False
  
  def nightVoteWarewolf(self,i,names,history=None):
    # self.getContext(self.names[i],True)
    voteContext = ""
    sr = 1
    for key, value in self.contexts[self.names[i]].items():
        voteContext += f"{sr}) {key}: {value}\n"
        sr += 1
    if history is None:
      voteName = self.agents[i].brain.query(QUERY_NIGHT_SINGLE.format(self.agents[i].name,voteContext,names),name='QUERY_NIGHT_SINGLE')
    else: 
      voteName = self.agents[i].brain.query(QUERY_NIGHT.format(self.agents[i].name,voteContext,history,names),name='QUERY_NIGHT')
    try:
      vote = self.names.index(voteName)
    except:
      voteName = self.findName(voteName,self.names[i])
      vote = self.names.index(voteName)
    if(self.warewolf[self.ids[voteName]]):
      vote = random.choice([index for index, value in enumerate(self.warewolf) if value is False and self.alive[index]])
    self.votes[vote] += 1

  
  def sleep(self):
    for i in range(self.n):
      if(not self.alive[i] or self.warewolf[i]): continue
      self.agents[i].sleep()

  def wakeUp(self):
    for i in range(self.n):
      if(not self.alive[i] or self.warewolf[i]): continue
      self.agents[i].sleeping = False
  
  def nightVote(self):

    self.threadNight = threading.Thread(target=self.nightVoteContext)
    self.threadNight.start()
    # self.night_phase_show = True
    self.night_phase_japanese_show = True
    log("Currently it is Night, the Warewolves will kill a townfolk...\n")
    self.votes = [0]*self.n

    self.sleep()

    names = ""
    j = 1
    werewolves = 0
    for i in range(self.n):
      if(self.warewolf[i] and self.alive[i]): werewolves+=1
      if(self.warewolf[i]): continue
      if(not self.alive[i]): continue
      names = names + f"{j}) {self.names[i]}\n"
      j += 1
    names = names[:-1]
      
    voters = []
    for i in range(self.n):
      if(self.alive[i] and self.warewolf[i]):
        voters.append(i)

    self.assembleTavern(voters)

    context = []

    self.threadNight.join()

    self.threadDay = threading.Thread(target=self.dayVoteContext)
    self.threadDay.start()

    if(werewolves>1):

      for i in range(self.n):
        if(not self.alive[i] or not self.warewolf[i]): context.append("")
        else: 
            voteContext = ""
            sr = 1
            for key, value in self.contexts[self.names[i]].items():
                voteContext += f"{sr}) {key}: {value}\n"
                sr += 1
            context.append(voteContext[:-1])

      global MinDialogues
      MinDialoguesPrev = MinDialogues
      MinDialogues = 4

      conversation = self.groupConversation(context,voters,True)

      MinDialogues = MinDialoguesPrev

      threads = []
      for i in range(self.n):
          if(not self.warewolf[i] or not self.alive[i]): continue
          thread = threading.Thread(target=self.nightVoteWarewolf, args=(i,names,conversation,))
          thread.start()
          threads.append(thread)
      for thread in threads:
          thread.join()
    
    else: 
      for i in range(self.n):
        if(not self.warewolf[i] or not self.alive[i]): continue
        self.nightVoteWarewolf(i,names)
      self.waitAssemble(voters)

    kick = self.votes.index(max(self.votes))
    self.alive[kick] = 0
    self.kicked = self.names[kick]
    self.killing = True
    self.elimination = self.kicked
    threadObs = threading.Thread(target=self.addObservationAll, args=(f"{self.kicked} has been eliminated by the Warewolves on {calendar.day} during the Night Phase",))
    threadObs.start()
    log(f"{self.kicked} has been killed by the Warewolves\n\n")
    self.checkEnd()

    self.wakeUp()

  def addObservationAll(self,observation):
    threads = []
    for i in range(self.n):
        if(not self.alive[i]): continue
        thread = threading.Thread(target=self.agents[i].remember, args=(observation,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

  def nightVoteContext(self):
    threads = []
    for i in range(self.n):
        if(not self.alive[i] or not self.warewolf[i]): continue
        thread = threading.Thread(target=self.getContext, args=(self.names[i],True,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join() 

  def dayVoteContext(self):
    threads = []
    for i in range(self.n):
        if(not self.alive[i]): continue
        thread = threading.Thread(target=self.getContext, args=(self.names[i],False,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()     

  def dayVote(self):

    # self.voting_phase_show = True
    self.voting_phase_japanese_show = True
    log("Currently it is Day, the Villagers will lynch someone...\n")

    context = []
    voters = []
    for i in range(self.n):
      if(self.alive[i]):
        voters.append(i)

    self.assembleTavern(voters)

    # thread = threading.Thread(target=self.dayVoteContext)
    # thread.start()
    # thread.join()
    self.threadDay.join()

    for i in range(self.n):
       if(not self.alive[i]): context.append("")
       else: 
          voteContext = ""
          sr = 1
          for key, value in self.contexts[self.names[i]].items():
              voteContext += f"{sr}) {key}: {value}\n"
              sr += 1
          context.append(voteContext[:-1])

    conversation = self.groupConversation(context,voters)

    votes = [0]*self.n
    log()
    prev = None
    # remainingTownfolk = getDetails(self)
    # remainingWarewolf = getDetails(self,True)  
    for i,voteId in enumerate(voters):
      #print("Agent",i)
      #print(voteId)
      #print(context[voteId])
      cover = "Warewolf" if self.warewolf[voteId] else "Townfolk"
      names = ""
      j = 1
      for id in voters:
        if(id==voteId): continue
        if(self.warewolf[voteId]):
          idCover = "Warewolf" if self.warewolf[id] else "Townfolk"
          names = names + f"{j}) {self.names[id]} - {idCover}\n"
        else:
          names = names + f"{j}) {self.names[id]}\n"
        j += 1
      names = names[:-1]
      # remaining = remainingWarewolf if cover is "Warewolf" else remainingTownfolk
      voteName = self.agents[voteId].brain.query(
         QUERY_DAY.format(self.agents[voteId].name,context[voteId],
                          conversation,self.agents[voteId].name,cover,
                          names,self.agents[voteId].name,self.agents[voteId].name,self.agents[voteId].name),name='QUERY_DAY')
      try:
        vote = self.names.index(voteName)
      except:
        voteName = self.findName(voteName,self.names[voteId])
        vote = self.names.index(voteName)
      log(f"{self.agents[voteId].name} voted to kick out {voteName}")
      threadObs = threading.Thread(target=self.addObservationAll, args=(f"{self.agents[voteId].name} voted to lynch {voteName} on {calendar.day} during the day phase",))
      threadObs.start()
      votes[vote] += 1
      if prev is not None: self.agents[prev].isSpeaking = False
      self.agents[voteId].isSpeaking = True
      self.agents[voteId].msg = f"I vote to kick out {voteName}"
      prev = voteId
      time.sleep(0.5)
      # self.agents[voteId].speech_bubble()
      # self.agents[voteId].draw()
      # pygame.display.update()

    #print()
    # vote = extractImportance(agents[voteId].brain.query(QUERY_DAY.format(agents[voteId].name,context[voteId],conversation))) - 1
    #if(vote>=i): vote += 1
    # print(agents[voteId].name,"voted to kick out",self.names[voters[vote]])

    maxVotes = max(votes)
    if(votes.count(maxVotes)>1):
      log("\nNobody was lynched")
      self.nobodyLynch = True
      threadObs = threading.Thread(target=self.addObservationAll, args=(f"Nobody was lynched on {calendar.day} during the day phase",))
      threadObs.start()
    else:
      kick = votes.index(maxVotes)
      self.alive[kick] = 0
      self.kicked = self.names[kick]
      self.farewell = True
      self.killing = True
      self.elimination = self.names[kick]
      log()
      log(f"{self.kicked} has been lynched by the Villagers")
      kickedCover = "Werewolf" if self.warewolf[kick] else "Townfolk"
      threadObs = threading.Thread(target=self.addObservationAll, args=(f"{self.kicked} has been lynched on {calendar.day} during the day phase.\n{self.kicked} was a {kickedCover}",))
      threadObs.start()

    for agent in self.agents:
      agent.location_name = 'Tavern'
      agent.dest = None
      agent.isSpeaking = False

    self.checkEnd()
      

  def findName(self,currName,voterName=None):
    for name in self.names:
      if(voterName is not None and name==voterName): continue
      if name in currName or currName in name:
        return name
    for name in self.names:
      if(voterName is not None and name==voterName): continue
      if name.split(' ')[0] in currName:
        return name
    raise Exception(f"Invalid Name - {currName}")

  def groupConversation(self, context, voters, night=False):
      history = ""

      if(night):
        remainingTownfolk = getNames(self,True)
        remainingWarewolf = getNames(self,False)
      else:
        remainingTownfolk = getDetails(self)
        remainingWarewolf = getDetails(self,True)         

      curr = random.choice(voters)
      votersN = len(voters)

      if(night):
        reply = self.agents[curr].nightconv_init(context[curr],remainingTownfolk,remainingWarewolf)
      else:
        remaining = remainingWarewolf if self.warewolf[curr] else remainingTownfolk
        reply = self.agents[curr].groupconv_init(self.kicked,context[curr],remaining)

      try:
        replyMsg = extract_dialogue(reply)
      except: 
        replyMsg = reply

      global Clock_Speed

      self.waitAssemble(voters)

      Clock_Speed = 1

      thread = threading.Thread(target=self.speak, args=(replyMsg,curr,))
      thread.start()
      self.agents[curr].msg = replyMsg 
      # self.agents[curr].isSpeaking = True 
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
          if(dialogues>MaxDialogues): break
          if(dialogues<MinDialogues): 
            QUERY = QUERY_GROUPCONV_MODERATOR
            queryName = 'QUERY_GROUPCONV_MODERATOR'
          else: 
            QUERY = QUERY_GROUPCONV_MODERATOR_END
            queryName = 'QUERY_GROUPCONV_MODERATOR_END'
          # currName = moderator.query(QUERY.format(history,names))
          
          if(votersN>2):
            currName = moderator.query(QUERY.format('\n'.join(lastFew[:2]),names),name=queryName)
            if("End Conversation" in currName): break
            try:
              curr = self.ids[currName]
            except:
              try:
                currName = self.findName(currName)
                curr = self.ids[currName]
              except:
                break
          else:
            EndScore = extractImportance(moderator.query(QUERY_GROUPCONV_END.format('\n'.join(lastFew[:2])),name='QUERY_GROUPCONV_END'))
            if(dialogues+EndScore>10): break
            if(dialogues==4): break 
            curr = voters[1-voters.index(curr)]
          
          if(night):
            reply = self.agents[curr].nightconv(context[curr], '\n'.join(lastFew[:3]), remainingTownfolk, remainingWarewolf)
          else:
            remaining = remainingWarewolf if self.warewolf[curr] else remainingTownfolk
            reply = self.agents[curr].groupconv(self.kicked, context[curr], '\n'.join(lastFew[:3]), remaining)

          if(prev!=curr):
            try:
              rating += getResponseRating(lastFew[-1], reply, self.contexts[self.names[curr]][self.names[prev]], self.names[prev], self.names[curr])
              rating_n += 1
            except:
              pass
          thread.join()
          try:
            replyMsg = extract_dialogue(reply)
          except: 
            replyMsg = reply
          thread = threading.Thread(target=self.speak, args=(replyMsg,curr,))
          thread.start()
          # reply = self.agents[curr].groupconv(self.kicked, context[curr], history)
          # self.agents[prev].isSpeaking = False 
          self.agents[curr].msg = replyMsg 
          # self.agents[curr].isSpeaking = True  
          # self.draw_window()
          prev = curr
          history = history + '\n'
          for i in range(self.n):
            if(self.alive[i]): self.agents[i].remember(reply)
      log("\nEnd of Conversation")
      if(rating_n==0): self.convRating = 0
      else: self.convRating = rating/rating_n 
      log(f"\nConversation Rating - {self.convRating}")
      log(f"Turn Taking Ratio - {get_turn_taking_ratio(history)}")
      log(f"Response Relevance - {calculate_response_relevance(history)}")
      log(f"Agreement Metric - {calculate_agreement_metric(history)}")
      thread.join()
      # self.agents[prev].isSpeaking = False 
      Clock_Speed = self.ClockPrev
      self.playBgMusic()
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

  def waitAssemble(self, voters):
    n = len(voters)
    wait = True 
    while wait:
      wait = False
      for i in range(n):
        if len(self.agents[voters[i]].destination_path)!=0:
          wait = True 
          break
      time.sleep(0.1) 

  def afternoon(self):
    # self.day_phase_show = True
    self.day_phase_japanese_show = True
    threadPlan = threading.Thread(target=self.generatePlanDay)
    threadPlan.start()   
    planGen = False   
    first = True
    while True:
      if(calendar.dt.hour in [11]): break
      if(calendar.dt.minute==0):
        now = calendar.time
        if(not planGen):
           threadPlan.join()
           planGen = True
        threads = []
        for i in range(self.n):
            if(not self.alive[i]): continue
            self.agents[i].task = None
            self.agents[i].taskReach = False
            thread = threading.Thread(target=self.agents[i].nextLocation, args=(now,self,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        self.observe(now)

        # if(first):
        #   first = False
        #   self.threadNight = threading.Thread(target=self.nightVoteContext)
        #   self.threadNight.start()

        # calendar.incrementMins(30)
      time.sleep(0.3)
      # self.taskOccupied = {hub:[False]*(len([node for node in nodes.keys() if "task" in node and hub in node])) for hub in hubs}
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
            if(self.agents[i].task is not None and self.agents[j].task is not None and not self.agents[i].busy and not self.agents[j].busy):  
              threadConv = threading.Thread(target=self.conversation, args=(self.names[i],self.names[j],))
              threadConv.start()   

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
      log('\n=== TOWNFOLKS WIN ===')
      self.townfolks_win_japanese_show = True
      time.sleep(5)
      self.run = False
      pygame.quit()
    if(players[1]>=players[0] or (not self.Night and players[1]>=players[0]-1)):
      log('\n=== WAREWOLVES WIN ===')
      self.warewolves_win_japanese_show = True
      time.sleep(5)
      self.run = False 
      pygame.quit()
          
    
  def switchPhase(self):
    self.changePhase = True

  def conversation(self, name1, name2):
    global Clock_Speed
    Clock_Speed = 1
    self.convs+=1
    names = [name1,name2]
    curr = 0
    agents = [self.agents[self.ids[name1]], self.agents[self.ids[name2]]]
    agents[0].busy = True 
    agents[1].busy = True
    thread1 = threading.Thread(target=self.getSingleContext, args=(name1,name2,))
    thread1.start()
    thread2 = threading.Thread(target=self.getSingleContext, args=(name2,name1,))
    thread2.start()
    thread1.join() 
    thread2.join()
    observation = f"{agents[curr].name} saw {agents[1-curr].name} {nodes[agents[1-curr].task]} at {calendar.time}"
    reply = agents[curr].talk_init(agents[1-curr].name, observation, self.contexts[names[curr]][names[1-curr]])
    while(not agents[0].taskReach or not agents[1].taskReach):
      time.sleep(0.2)
    if(agents[0].task==agents[1].task):
      dest1 = agents[0].destination
      dest2 = agents[1].destination
      agents[0].destination_path.append((agents[0].x-25,agents[0].y))
      agents[1].destination_path.append((agents[1].x+25,agents[1].y))
    try:
      replyMsg = extract_dialogue(reply)
    except: 
      replyMsg = reply
    agents[curr].msg = replyMsg 
    agents[curr].isSpeaking = True
    history = ""
    lastFew = []
    conv_n = 0
    moderator = GPT()
    while reply is not None:
        log(reply)
        lastFew.append(reply)
        conv_n += 1
        EndScore = extractImportance(moderator.query(QUERY_GROUPCONV_END.format('\n'.join(lastFew[:2])),name='QUERY_GROUPCONV_END'))
        if(conv_n+EndScore>10): break
        history = history + '\n' + reply
        curr = 1 - curr
        reply = agents[curr].talk(agents[1-curr].name, reply, '\n'.join(lastFew[:3]), self.contexts[names[curr]][names[1-curr]], conv_n)
        if(reply is None): break
        try:
          replyMsg = extract_dialogue(reply)
        except: 
          replyMsg = reply
        agents[curr].msg = replyMsg 
        agents[1-curr].isSpeaking = False
        agents[curr].isSpeaking = True
        history = history + '\n'
    log("\nEnd of Conversation")
    self.convs-=1
    agents[0].isSpeaking = False 
    agents[1].isSpeaking = False 
    agents[0].busy = False 
    agents[1].busy = False
    if(agents[0].task==agents[1].task):
      agents[0].destination = dest1
      agents[1].destination = dest2
    if(not self.convs): Clock_Speed = self.ClockPrev

  # def startNight(self):

  def reset(self) : 
      for agent in self.agents:
         agent.graphics_init(self.win)
      self.run = True

  def draw_time(self) :
      timePrecise = calendar.dt.strftime("%I:%M:%S %p")
      text = f"{calendar.day}\n{timePrecise}"
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

  def playBgMusic(self):
    music = pygame.mixer.music.load(Path+'music.mp3')
    pygame.mixer.music.play(-1)
     
  
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
         self.agents[i].emoji_bubble(TASK_EMOJI_MAP[self.agents[i].task])

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

  
  def draw_nobody_lynch(self) :
      if(not self.nobodyLynch): return
      self.win.blit(self.black_bg,(0,0))
      text_surface = font2.render("Nobody was Lynched", True, WHITE)
      text_rect = text_surface.get_rect()
      text_rect.centerx = WIN_WIDTH // 2
      text_rect.centery = WIN_HEIGHT // 2
      self.win.blit(text_surface,text_rect)
      self.nobodyLynch = False
      pygame.display.update()
      time.sleep(3)     
  
  
  def draw_fps(self):
    self.fps = int(self.clock.get_fps())
    fps_text = font3.render(f"FPS: {self.fps}", True, (0, 85, 255))
    fps_text_rect = fps_text.get_rect(bottomright=(10+fps_text.get_width(), self.win.get_height() - 10))
    self.win.blit(fps_text, fps_text_rect)
    if(self.fps>15): self.VelFactor = FPS/self.fps
  
  def draw_window(self) : 

    if(self.warewolves_win_japanese_show):
      self.win.blit(self.warewolves_win_japanese,(0,0))
      pygame.display.update()
      return
    if(self.townfolks_win_japanese_show):
      self.win.blit(self.townfolks_win_japanese,(0,0))
      pygame.display.update()
      return

    self.win.blit(self.bg,(0,0))

    if(self.elimination is not None and not self.killing):
      self.drawElimination()

    if(not self.killing and self.elimination is None):

      self.draw_nobody_lynch()
      self.draw_phase()

      for i,player in enumerate(self.agents): 
          if(self.alive[i]):
              player.draw() 
      self.draw_fire()  
      for i,player in enumerate(self.agents): 
          if(self.alive[i]):
              player.drawBubble() 

      self.drawTaskEmoji()  

      self.draw_time()
      self.draw_fps()
      self.draw_hover()
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
      if(self.night_phase_japanese_show):
        # self.win.blit(self.night_phase,(0,0))
        # self.night_phase_show = False
        self.win.blit(self.night_phase_japanese,(0,0))
        self.night_phase_japanese_show = False
        calendar.night()
      elif(self.day_phase_japanese_show):
        # self.win.blit(self.day_phase,(0,0))
        # self.day_phase_show = False
        self.win.blit(self.day_phase_japanese,(0,0))
        self.day_phase_japanese_show = False
        if(calendar.dt.hour>20): calendar.nextDay()
        calendar.tasks()
      elif(self.voting_phase_japanese_show):
        # self.win.blit(self.voting_phase,(0,0))
        # self.voting_phase_show = False
        self.win.blit(self.voting_phase_japanese,(0,0))
        self.voting_phase_japanese_show = False
        if(calendar.dt.hour>20): calendar.nextDay()
        calendar.voting()
      elif(self.start_phase_show):
        self.win.blit(self.start_phase,(0,0))
        self.start_phase_show = False
      elif(self.townfolks_win_japanese_show):
        self.win.blit(self.townfolks_win_japanese,(0,0))
        self.townfolks_win_japanese_show = False
      elif(self.warewolves_win_japanese_show):
        self.win.blit(self.warewolves_win_japanese,(0,0))
        self.warewolves_win_japanese_show = False
      elif(self.end_phase_show):
        self.win.blit(self.end_phase,(0,0))
        self.end_phase_show = False
      else:
         return
      pygame.display.update()
      time.sleep(4)

  def draw_hover(self):
    for key in hover_dict:
      if hover_dict[key].hovered:
        hover_dict[key].hover_bubble(self.win)

  def nextDay(self):
     calendar.nextDay()
     calendar.dt = calendar.dt.replace(hour=7, minute=30)
     
  def handleHovers(self,event):
    for key in hover_dict:
      hover_dict[key].handle_event(event)

      

  def step(self) :

      for event in pygame.event.get():
        if event.type == pygame.QUIT : 
          self.run = False
          pygame.quit()  

        self.handleHovers(event) 
      
      keys = pygame.key.get_pressed()
      # self.agents[0].manual_move(keys)

      for i,player in enumerate(self.agents): 
          if(self.alive[i]):
              player.move(self.VelFactor) 
      
      if(self.changePhase):
        self.stepPhase()

      if(self.killing):
        self.stepKilling()

      self.draw_window()
      
      calendar.increment(self.VelFactor*Clock_Speed/FPS)

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
    
                  
                
   