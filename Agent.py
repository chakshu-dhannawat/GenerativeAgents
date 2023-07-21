from Memories import calendar, Memory, Reflection
from Queries import *
from Params import *
from Util import *
from Graph import Graph,town
from GPT import GPT
from Game import *
from DatabaseHandler import DB
import os
import pygame
import random
import math
import emoji
import time

from Generate_voiceover import generate_voiceover

class Agent():

  def __init__(self, name, summary, graphics):
    self.name = name
    self.summary = summary
    self.location = Initial
    self.memory = [Memory(obs.strip()) for obs in summary.split(';')]
    self.brain = GPT(context=CONTEXT_AGENT)
    self.inPopup_house1 = False
    self.inPopup_house2 = False
    self.werewolf = False
    self.task = None
    self.taskReach = False
    self.now = None
    self.busy = False
    self.hub = None
    self.plan = None
    self.board = False

    self.sheriff = False
    if "werewolf" in summary:
      self.werewolf = True
      QUERY_INIT = QUERY_INIT_WEREWOLF.format(name, name, summary, name, details)
      for player in details.split('\n'):
        self.remember(player.split(') ')[1])
    else: QUERY_INIT = QUERY_INIT_TOWNFOLK.format(name, name, summary, name)
    self.strategy = self.brain.query(QUERY_INIT,name='QUERY_INIT')

    log(f"{self.name}'s Strategy for {calendar.day} -\n\n{self.strategy}\n\n-----------------------\n\n")
    # self.action = self.brain.query(QUERY_ACTION.format(name, summary, self.plan, Initial, calendar.time, getNames(), getPeople()))
    # print(f"\n{self.name}'s Action for next hour -\n{self.action}")
    # self.result = self.brain.query(QUERY_PAST_TENSE.format(name, name))
    # print(f"\n{self.name}'s Result of Action for next hour -\n{self.result}")
    strategies = extractQuestions(self.strategy)

    for strat in strategies:
      self.remember(strat)
    # log('\n-----------------------\n')

    self.graphics = graphics
    self.Character_Size = None

  def nextHourPlan(self,now):
     keys = list(self.plan.keys())
     try:
      nextKey = keys(keys.index(now)+1)
     except:
      return ""
     return self.plan(nextKey)

  def generatePlanDay(self):
    if(self.werewolf):
      self.plan =  extractPlan(self.brain.query(QUERY_PLAN_WEREWOLVES.format(self.name, self.summary, getHubs(),getAllTasks(True), self.name),remember=False,name='QUERY_PLAN'))
    else:
      self.plan =  extractPlan(self.brain.query(QUERY_PLAN_TOWNFOLK.format(self.name, self.summary, getHubs(),getAllTasks(False), self.name),remember=False,name='QUERY_PLAN'))
    printPlan(self.plan,self.name,calendar.day)

  def graphics_init(self,win):

    self.win = win
    self.x = self.graphics['x']
    self.y = self.graphics['y']
    self.width = self.graphics['width']
    self.height = self.graphics['height']
    self.vel = Character_Speed
    self.vel_x = Character_Speed / math.sqrt(2)
    self.vel_y = self.vel_x
    self.left = True
    self.right = False
    self.walkCount = 0
    self.standing = True
    self.hitbox = (self.x + 17, self.y + 11, 29, 52)
    self.walkRight = []
    self.walkLeft = []
    self.walkUp =[]
    self.walkDown=[]
    self.dest = None 

    self.char = None
    self.up = False
    self.down = False
    

    self.was_left = False
    self.was_right = False

    self.walkTimer = random.randint(2000, 3000)  # Random timer between 2000ms and 3000ms
    self.timer = 0
    self.directionTimer = self.walkTimer

    self.folder_name = self.graphics['folder_name']

    self.location_name = self.graphics['initialLocation']
    self.destination=None
    self.destination_x=-10
    self.destination_y=-10
    self.is_travelling = False
    self.destination_path=[]
    # Speaking Bubbles
    self.isSpeaking = False
    self.msg = None
    self.sleeping = False
    self.sleepSoon = False
    
    self.walkRight, self.walkLeft, self.walkUp, self.walkDown, self.char = self.graphics_load()
    # self.walkRight, self.walkLeft, self.char = walkRight, walkLeft, char
    self.choose_random_location()   

  def animationKillInit(self):
    self.kill_x = -self.char_rect.width
    self.kill_y = WIN_HEIGHT // 2 - self.char_rect.height // 2
    self.killRotationAngle = 0
    self.killSpeed = 12
    self.killRotationSpeed = 5

  def animationKillStep(self):
    self.kill_x += self.killSpeed
    self.killRotationAngle += self.killRotationSpeed
    rotated_image = pygame.transform.rotate(self.char, self.killRotationAngle)
    self.win.blit(rotated_image, (self.kill_x, self.kill_y))
  
  def remember(self,observation):
    #self.memory.append(Memory(observation.strip()))
    DB.addMemories(self.name, Memory(observation.strip()))

  def talk_context(self,person):
    relevant_memories = getRetrievedMemories(self.retrieve(f"What is {self.name}'s relationship with {person}",N_Memories))
    self.context = self.brain.query(QUERY_CONTEXT.format(relevant_memories,self.name,person),remember=False,name='QUERY_CONTEXT')

  def vote_context(self,person,n_memory=N_Memories):
    relevant_memories = getRetrievedMemories(self.retrieve(f"What is {self.name}'s observations about {person}",n_memory))
    return self.brain.query(QUERY_CONTEXT.format(relevant_memories,self.name,person),remember=False,name='QUERY_CONTEXT')

  def nightconv_init(self,context,remainingT,remainingW):
    dialogue = self.brain.query(QUERY_NIGHTCONV_INIT.format(self.name,context,remainingT,remainingW,self.name,self.strategy,self.name,self.name,self.name),remember=False,name='QUERY_NIGHTCONV_INIT')
    dialogue = dialogue.replace('\n', '')
    return dialogue

  def nightconv(self,context,history,remainingT,remainingW):
    dialogue = self.brain.query(QUERY_NIGHTCONV_REPLY.format(self.name,context,history,remainingT,remainingW,self.name,self.strategy,self.name,self.name,self.name),remember=False,name='QUERY_NIGHTCONV_REPLY')
    dialogue = dialogue.replace('\n', '')
    return dialogue

  def groupconv_init(self,kicked,context,remaining):
    cover = "werewolf" if self.werewolf else "Townfolk"
    dialogue = self.brain.query(QUERY_GROUPCONV_INIT.format(kicked,self.name,context,remaining,self.name,self.strategy,self.name,cover,self.name,self.name,self.name),remember=False,name='QUERY_GROUPCONV_INIT')
    dialogue = dialogue.replace('\n', '')
    return dialogue

  def groupconv(self,kicked,context,history,remaining):
    cover = "werewolf" if self.werewolf else "Townfolk"
    dialogue = self.brain.query(QUERY_GROUPCONV_REPLY.format(kicked,self.name,context,history,remaining,self.name,self.strategy,self.name,cover,self.name,self.name,self.name),remember=False,name='QUERY_GROUPCONV_REPLY')
    dialogue = dialogue.replace('\n', '')
    return dialogue

  def talk_init(self,person,observation,context):
    dialogue = self.brain.query(QUERY_DIALOGUE_INIT.format(self.name,person,calendar.day,calendar.time,self.name,nodes[self.task],observation,self.name,context,person,self.name,self.name),remember=False,name='QUERY_DIALOGUE_INIT')
    dialogue = dialogue.replace('\n', '')
    self.remember(dialogue)
    return dialogue

  def talk(self,person,last_dialogue,history,context,n_conv):
    self.remember(last_dialogue)
    dialogue = self.brain.query(QUERY_DIALOGUE_REPLY.format(calendar.day,calendar.time,self.name,nodes[self.task],person,self.name,self.name,context,history,person,self.name,self.name,n_conv,self.name),remember=False,name='QUERY_DIALOGUE_REPLY')
    dialogue = dialogue.replace('\n', '')
    if("End Conversation" in dialogue): return None
    self.remember(dialogue)
    return dialogue

  def nextDay(self):
    #TODO
    pass
    # tomm = getNextDay(self.day)
    # self.plan = self.brain.query(f"Name: {self.name}. {self.name} lives in {self.environment}. {self.summary}.\n On {self.day}, {self.name} {self.plan}.\n Today is {tomm}.\n\nHere is {self.name}’s plan today as human in broad strokes: 1) ")
    # self.plan = "1) " + self.plan.split('\n\n')[0]
    # self.day = tomm
    # print(f"{self.name}'s Plan for {self.day} -\n\n{self.plan}\n")

  def detailedPlan(self):
    self.hourly = extractPlan(self.brain.query(f"{self.name}'s Plan for {calendar.day} -\n{self.plan}\n\ndecompose the plan for {calendar.day} to create hour-long chunks of actions. The chunks should be exactly of one hour, not more not less."))
    for t in self.hourly.keys():
      log(f'{t} : {self.hourly[t]}')
    log('\n\n')
    self.MinutePlan = {}
    for hour in self.hourly.keys():
      detailed = self.brain.query(f'decompose the {hour} plan into 5 to 20 minute chunks. decompose in maximum 6 chunks. The overall plan for {hour} is - {self.hourly[hour]}',remember='False')
      detailed = extractPlan(detailed)
      for t in detailed.keys():
        try:
          detailed[t] = self.brain.query(f'Convert this to past tense with the name {self.name} (for example - "drink coffee" becomes "{self.name} drank coffee) -\n 1)"{detailed[t]}"',remember='False')
          # if(detailed[t][0]=='"'): detailed[t] = detailed[t][1:-1]
        except:
          pass
        log(f'{t} : {detailed[t]}')
      self.MinutePlan.update(detailed)
    return self.MinutePlan

  def retrieve(self, query, n):
    score = []
    memories_data = DB.getAllMemories(self.name)
    for mem in memories_data:
      score.append(mem.retrievalScore(query))
    ids = sorted(range(len(score)), key=lambda i: score[i], reverse=True)[:n]
    memories = []
    for id in ids:
      memories.append(memories_data[id].observation)
      # print(memories_data[id].lastAccess)
      DB.updateMemories(self.name,memories_data[id]._id,'lastAccess',calendar.dt)
      
      # self.memory[id].lastAccess = calendar.dt
    m = ""
    for i,mem in enumerate(memories): m += f"{i+1}) {mem}\n"
    # log(f"Query -\n{query}\nRetrieved Memories-\n{m}")
    return memories

  def reflect(self,n_questions=N_Questions, n_memories=N_Memories, n_reflections=N_Reflections):
    questions = extractQuestions(self.brain.query(QUERY_REFLECT_QUESTIONS.format(getMemories(self.memory),n_questions),remember=False,name='QUERY_REFLECT_QUESTIONS'))
    for question in questions:
      if(question==''): continue
      memories = self.retrieve(question,n_memories)
      insights = extractQuestions(self.brain.query(QUERY_REFLECT_INSIGHTS.format(self.name,getRetrievedMemories(memories),n_reflections),remember=False,name='QUERY_REFLECT_INSIGHTS'))
      for insight in insights:
        if(insight==''): continue
        #TODO: Add child nodes
        self.memory.append(Reflection(insight))

  def nextLocation(self,now,game):
    # self.destination_path = self.destination_path + town.shortestPath(self.location_name,"Tavern")
    # move agent to tavern in start of afternoon phase
    try: 
      locationName = self.brain.query(QUERY_LOCATION.format(now,self.name,now,self.plan[timeKey(now)],getHubs(),self.name,self.name),remember=False,name='QUERY_LOCATION')
    except:
      locationName = random.choice(hubs) 
    # locationName = self.brain.query(QUERY_LOCATION.format(now,self.name,now,random.choice(list(self.plan.values())),self.name,getHubs()),remember=False)
    newLocation = extractHub(locationName)
    if(newLocation=="Tavern"): newLocation = random.choice(hubs)
    log(f"\n{self.name} chose to go to {newLocation} at {calendar.time}\n")
    self.remember(f"\n{self.name} chose to go to {newLocation} at {calendar.time}\n")
    # self.dest = newLocation
    self.hub = newLocation
    tasks, tasksList = getTasks(newLocation,game,self.werewolf)
    # print(self.name,tasksList,self.werewolf)
    if(len(tasksList)==0):
       self.task = None
       self.dest = 'Hut 1 Intermediate03'
       log(f"No Tasks at {newLocation}")
       return
    try: 
      if(self.werewolf): QUERY_TASK = QUERY_TASK_WEREWOLF
      else: QUERY_TASK = QUERY_TASK_TOWNFOLK
      taskSr = extractImportance(self.brain.query(QUERY_TASK.format(now,self.name,now,self.plan[timeKey(now)],self.name,tasks),remember=False,name='QUERY_TASK'))
         
    except:
      self.task = None
      self.dest = 'Hut 1 Intermediate03'
      log(f"{self.name} could not choose a Task at {newLocation}")
      return 
    # print(taskSr)
    # tasksList = [node for node in town.graph[newLocation] if "task" in node]
    # game.taskOccupied[newLocation][taskSr-1] = True
    try:
      newLocation = tasksList[taskSr-1]
    except:
      newLocation = tasksList[0]
    log(f"\n{self.name} chose to do the task : {newLocation} at {calendar.time}\n")
    self.remember(f"\n{self.name} chose to do the task : {newLocation} at {calendar.time}\n")
    # self.dest = newLocation
    self.dest = "List"
    self.board = True
    self.task = newLocation


  def graphics_load(self):
    self.Character_Size = random.choice(Character_Sizes)
    walk_right = []
    walk_left = []
    walk_up = []
    walk_down = []
    temp = None
    folder_path = Path + self.folder_name
    image_files = os.listdir(folder_path)

    #Detect if werewolf


    if self.werewolf:
       
      # Load images into walkRight, walkLeft, walkUp, walkDown arrays
      for file_name in image_files:
          if file_name.startswith('R'):
              temp = pygame.image.load(os.path.join(folder_path, file_name))
              temp = pygame.transform.scale(temp, self.Character_Size)
              outline_image = outline_character(temp)
              walk_right.append(outline_image)
          elif file_name.startswith('L'):
              temp = pygame.image.load(os.path.join(folder_path, file_name))
              temp = pygame.transform.scale(temp, self.Character_Size)
              outline_image = outline_character(temp)
              walk_left.append(outline_image)
          elif file_name.startswith('U'):
              temp = pygame.image.load(os.path.join(folder_path, file_name))
              temp = pygame.transform.scale(temp, self.Character_Size)
              outline_image = outline_character(temp)
              walk_up.append(outline_image)
          elif file_name.startswith('D'):
              temp = pygame.image.load(os.path.join(folder_path, file_name))
              temp = pygame.transform.scale(temp, self.Character_Size)
              outline_image = outline_character(temp)
              walk_down.append(outline_image)
      self.char_rect = walk_down[0].get_rect()
      return walk_right, walk_left, walk_up, walk_down, walk_down[0]
    
    else:
      # Townfolk
      # Load images into walkRight,walkLeft, walkUP, walkDown arrays
      for file_name in image_files:
          if file_name.startswith('R'):
              # self.bg = pygame.transform.scale(bg, DEFAULT_IMAGE_SIZE)
              temp = pygame.image.load(os.path.join(folder_path, file_name))
              temp = pygame.transform.scale(temp, self.Character_Size)
              walk_right.append(temp)
          elif file_name.startswith('L'):
              temp = pygame.image.load(os.path.join(folder_path, file_name))
              temp = pygame.transform.scale(temp, self.Character_Size)
              walk_left.append(temp)
          elif file_name.startswith('U'):
              temp = pygame.image.load(os.path.join(folder_path, file_name))
              temp = pygame.transform.scale(temp, self.Character_Size)
              walk_up.append(temp)
          elif file_name.startswith('D'):
              # walk_down.append(pygame.image.load(os.path.join(folder_path, file_name)))
              temp = pygame.image.load(os.path.join(folder_path, file_name))
              temp = pygame.transform.scale(temp, self.Character_Size)
              walk_down.append(temp)
      self.char_rect = walk_down[0].get_rect() 
      return walk_right, walk_left, walk_up, walk_down, walk_down[0]
      



  def drawBubble(self):
     if(self.sleeping): return
     if self.isSpeaking:
          self.speech_bubble()
  
  def draw(self):
      
      # if(self.sleeping): return
      
      if self.walkCount + 1 >= 30:
          self.walkCount = 0

      if not(self.standing):
          if self.left:
              self.win.blit(self.walkLeft[self.walkCount//10], (int(self.x),int(self.y)))
              self.walkCount += 1
          elif self.right:
              self.win.blit(self.walkRight[self.walkCount//10], (int(self.x),int(self.y)))
              self.walkCount +=1
          elif self.up:
              self.win.blit(self.walkUp[self.walkCount//10], (int(self.x),int(self.y)))
              self.walkCount += 1
          elif self.down:
              self.win.blit(self.walkDown[self.walkCount//10], (int(self.x),int(self.y)))
              self.walkCount += 1
      else:
          self.win.blit(self.char, (int(self.x), int(self.y)))
      if self.sheriff:
         self.win.blit(sheriff_badge, (int(self.x-15), int(self.y-15)))

  # def move(self,VelFactor):
  #     if(self.sleeping): return
  #     #If agent has reached location
  #     if(abs(self.x - self.destination_x)<1 and abs(self.y - self.destination_y)<1):
  #         self.left=False
  #         self.right=False
  #         self.up=False
  #         self.down = False
  #         self.standing=True
  #         self.location_name = self.destination
  #         self.is_travelling=False
          
          
  #     # Move towards the destination
  #     if self.is_travelling:
          
  #         # Calculate the slope between the current position and the destination
  #         # slope = (self.destination_y - self.y) / (self.destination_x - self.x)

  #         # Calculate theta from the slope
  #         # theta = math.atan(slope)
  #         theta = math.atan2(self.destination_y - self.y, self.destination_x - self.x)
  #         self.vel_x = abs(math.cos(theta) * Character_Speed * VelFactor)
  #         self.vel_y = abs(math.sin(theta) * Character_Speed * VelFactor)
          
  #         if self.destination_x-self.x>1+int(self.vel_x):
  #             self.right=True
  #             self.left=False
  #         elif self.x-self.destination_x>1+int(self.vel_x):
  #             self.left = True
  #             self.right = False
  #         else:
  #             if(self.right):
  #                 self.right=False
  #                 self.left = False
  #                 self.was_right=True
  #             else:
  #                 self.right=False
  #                 self.left = False
  #                 self.was_left=True
  #         if self.destination_y-self.y>1+int(self.vel_y):
  #             self.down = True
  #             self.up = False
  #         elif self.y-self.destination_y>1+int(self.vel_y):
  #             self.up=True
  #             self.down=False
  #         else:
  #             self.up=False
  #             self.down = False
          
          

  #         # print(self.name, self.x)
  #         # print(self.name, self.y)
  #         if self.left and self.x > Character_Speed * VelFactor:
  #             self.x -= self.vel_x
  #             self.standing = False
  #         if self.right and self.x < WIN_WIDTH - Character_Speed * VelFactor:
  #             self.x += self.vel_x
  #             self.standing = False
  #         if self.up and self.y > Character_Speed * VelFactor:
  #             self.y -= self.vel_y
  #             self.standing = False
  #             # self.left=True
  #         if self.down and self.y < WIN_HEIGHT - Character_Speed * VelFactor:
  #             self.y += self.vel_y
  #             self.standing = False
  #             # self.right=True
  #         self.standing = not(self.left or self.right or self.up or self.down)

  #     #Random choice to stay in that location or move
  #     else:
        
  #         self.timer+=1
  #         if(self.timer>50):
  #             self.timer=0
  #         #     change_location = random.choice(['Move', 'Stay'])
  #         #     if(change_location == 'Move'):
  #         #         while self.location_name == self.destination:
  #         #             self.choose_random_location()
  #         #             self.is_travelling = True
  #         # self.destination_path.pop(0)
          
  #         if len(self.destination_path)==0:

  #           if(self.destination==self.task): self.taskReach = True

  #           if(self.dest is None):
  #             self.choose_random_location()
              
  #           elif(self.dest != "Stop"):
  #             self.choose_location(self.dest)

  #           if(self.sleepSoon and self.location_name in ["Hut 1","Hut 2"]):
  #             self.sleepSoon = False
  #             self.sleeping = True

  #         else:
  #           # self.isSpeaking=True
  #           # self.msg = "I want to travel to"+ str(self.destination_path[-1])
  #           # self.speech_bubble()
  #           # self.draw()
  #           # pygame.display.update()
  #           self.destination = self.destination_path[0]
  #           self.destination_path.pop(0)
            
  #           try:
  #             self.destination_x, self.destination_y = LOCATION_MAP[self.destination]
  #           except:
  #             self.destination_x, self.destination_y = self.destination
  #           self.is_travelling=True
            
  def move(self, VelFactor):
      if(self.sleeping): return
      #If agent has reached location
      if(abs(self.x - self.destination_x)<1+int(self.vel_x) and abs(self.y - self.destination_y)<1+int(self.vel_y)):
          self.left=False
          self.right=False
          self.up=False
          self.down = False
          self.standing=True
          self.location_name = self.destination
          self.is_travelling=False
          
          
      # Move towards the destination
      if self.is_travelling:
          
          # Calculate the slope between the current position and the destination
          # slope = (self.destination_y - self.y) / (self.destination_x - self.x)

          # Calculate theta from the slope
          # theta = math.atan(slope)
          theta = math.atan2(self.destination_y - self.y, self.destination_x - self.x)
          self.vel_x = abs(math.cos(theta) * self.vel * VelFactor)
          self.vel_y = abs(math.sin(theta) * self.vel * VelFactor)


          if self.destination_x-self.x>1+int(self.vel_x):
              self.right=True
              self.left=False
          elif self.x-self.destination_x>1+int(self.vel_x):
              self.left = True
              self.right = False
          else:
              if(self.right):
                  self.right=False
                  self.left = False
                  self.was_right=True
              else:
                  self.right=False
                  self.left = False
                  self.was_left=True
          if self.destination_y-self.y>1+int(self.vel_y):
              self.down = True
              self.up = False
          elif self.y-self.destination_y>1+int(self.vel_x):
              self.up=True
              self.down=False
          else:
              self.up=False
              self.down = False
          
          

          # print(self.name, self.x)
          # print(self.name, self.y)
          if self.left and self.x > self.vel_x:
              self.x -= self.vel_x
              self.standing = False
          if self.right and self.x < WIN_WIDTH - self.vel_x:
              self.x += self.vel_x
              self.standing = False
          if self.up and self.y > self.vel_y:
              self.y -= self.vel_y
              self.standing = False
              # self.left=True
          if self.down and self.y < WIN_HEIGHT - self.vel_y:
              self.y += self.vel_y
              self.standing = False
              # self.right=True
          self.standing = not(self.left or self.right or self.up or self.down)

      #Random choice to stay in that location or move
      else:
        
          self.timer+=1
          if(self.timer>50):
              self.timer=0
          #     change_location = random.choice(['Move', 'Stay'])
          #     if(change_location == 'Move'):
          #         while self.location_name == self.destination:
          #             self.choose_random_location()
          #             self.is_travelling = True
          # self.destination_path.pop(0)
          
          if len(self.destination_path)==0:

            if(self.board and self.destination=="List"):
               self.board = False 
               self.dest = self.task
            
            if(not self.taskReach and self.destination==self.task): 
              # if("Sleeping" in self.task): return
              self.taskReach = True
              taskCompleted[self.task] = True
              if("Bucket_Sabotage" in TASK_EMOJI_MAP[self.task]): 
                self.game.tasksDone -= 1
                location = random.choice(["Well task01", "Well task02"])
                taskCompleted[location] = False
            
              elif("Fence_Sabotage" in TASK_EMOJI_MAP[self.task]): 
                self.game.tasksDone -= 1
                location = random.choice(["Cattle Farm task01", "Cattle Farm task03", "Cattle Farm task04"])
                taskCompleted[location] = False

              elif("Broom_Sabotage" in TASK_EMOJI_MAP[self.task]): 
                self.game.tasksDone -= 1
                location = random.choice(["Shrine task01", "Shrine task02", "Shrine task03"])
                taskCompleted[location] = False
                
              elif("FishingPole_Sabotage" in TASK_EMOJI_MAP[self.task]): 
                self.game.tasksDone -= 1
                location = random.choice(["Fishing Pond task02", "Fishing Pond task03", "Fishing Pond task04"])
                taskCompleted[location] = False

              elif("Electric_Sabotage" in TASK_EMOJI_MAP[self.task]): 
                self.game.tasksDone -= 1
                location = random.choice(["Electricity House task01", "Electricity House task02", "Electricity House task03"])
                taskCompleted[location] = False

              elif(not self.werewolf and not "Sleeping" in self.task): self.game.tasksDone += 1

            if(self.dest is None):
              # self.choose_random_location()
              pass
              
            elif(self.dest != "Stop" and self.dest != self.destination):
              self.choose_location(self.dest)
              # if(self.dest is not None and self.task is not None and self.dest==self.task): self.printPath()

            if(self.sleepSoon and self.location_name in SLEEPING_NODES):
              self.sleepSoon = False

              self.sleeping = True

          else:
            # self.isSpeaking=True
            # self.msg = "I want to travel to"+ str(self.destination_path[-1])
            # self.speech_bubble()
            # self.draw()
            # pygame.display.update()
            self.destination = self.destination_path[0]

            self.destination_path.pop(0)
            
            try:
              self.destination_x, self.destination_y = LOCATION_MAP[self.destination]
            except:
              self.destination_x, self.destination_y = self.destination
            self.is_travelling=True         
              
  def manual_move(self,keys):

      if (keys[pygame.K_a]) and (self.x > self.vel) : 
          self.x -= self.vel
          self.left = True
          self.right = False
          self.up=False
          self.down=False

      if (keys[pygame.K_d]) and (self.x < WIN_WIDTH - self.width - self.vel) : 
          self.x += self.vel
          self.right = True
          self.left = False
          self.up=False
          self.down=False

      if (keys[pygame.K_s]) and (self.y< WIN_WIDTH - self.height - self.vel): 
          self.y+= self.vel
          self.down = True
          self.up=False
          self.left=False
          self.right=False

      if (keys[pygame.K_w]) and (self.y > self.vel + 100) : 
          self.y-= self.vel
          self.up=  True
          self.down=False
          self.left=False
          self.right=False

      self.standing = not (keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d])

  def choose_random_location(self):
      # Randomly choose a new direction
      location = random.choice(list(LOCATION_MAP.keys()))
      if(not isinstance(self.location_name, str)): self.location_name = "Tavern"
      self.destination_path = town.shortestPath(self.location_name,location)
      
      # self.destination = self.destination_path[0]
      # self.destination_x, self.destination_y = LOCATION_MAP[self.destination]

  def choose_location(self,location):
      if(not isinstance(self.location_name, str)): self.location_name = "Tavern"
      self.destination_path = town.shortestPath(self.location_name,location)
      # self.destination = self.destination_path[0]
      # self.destination_x, self.destination_y = LOCATION_MAP[self.destination]

  def sleep(self):
      self.destination_path = []
      self.dest = random.choice(SLEEPING_NODES)
      self.task = self.dest
      self.sleepSoon = True

  def printPath(self):
      pathString = f"{self.name} : "
      for path in self.destination_path:
        pathString += f"{path} > "
      print(pathString)

  def tavern(self,point):
      (x,y) = point
      closest_index = min(range(len(TavernCoordinates)), key=lambda idx: (x - TavernCoordinates[idx][0]) ** 2 + (y - TavernCoordinates[idx][1]) ** 2)
      self.dest = "Stop"
      if(not isinstance(self.location_name, str)): self.location_name = "Tavern"
      self.destination_path = self.destination_path + town.shortestPath(self.location_name,TavernNodes[closest_index])
      
      # self.destination = self.destination_path[0]
      # self.destination_x, self.destination_y = LOCATION_MAP[self.destination]
      # self.destination_x, self.destination_y = point
      # self.is_travelling = True
      self.destination_path.append(point)
  
  def speech_bubble(self):
      text = self.msg
      x = self.x
      y = self.y
      bubble_image = pygame.image.load(Path+"speechbubble_png_blue.png")  # Replace "bubble.png" with the path to your predetermined image
      bubble_image2 = pygame.image.load(Path+"onevoneelectricspeechbubble.png")

      # Render the text
      font_size = 22  # Desired font size
      font = pygame.font.Font(None, font_size)

      # Split text into words
      words = text.split()

      # Create lines of text with a maximum of 6 words per line
      text_lines = []
      line = ""
      for word in words:
          if len(line.split()) < CONVERSATION_WORD_LIMIT:
              line += " " + word
          else:
              text_lines.append(line.strip())
              line = word
      text_lines.append(line.strip())

      # Calculate the maximum width and height for all lines
      max_width = 0
      total_height = 0
      for line in text_lines:
          text_surface = font.render(line, True, (0, 0, 0))
          max_width = max(max_width, text_surface.get_width())
          total_height += text_surface.get_height()

      # Create the bubble rectangle around the text
      bubble_padding = 20
      bubble_width = max_width + bubble_padding * 10
      bubble_height = total_height + bubble_padding * 4
      # bubble_rect = pygame.Rect(x - bubble_width // 2 - 50, y - bubble_height // 2 - 50, bubble_width, bubble_height)

      # Blit the bubble image onto the surface
      if(x<200):
        scaled_bubble_image = pygame.transform.scale(bubble_image2, (bubble_width, bubble_height))
        bubble_rect = scaled_bubble_image.get_rect(bottomleft=(x-bubble_width//4, y))
      else:
        scaled_bubble_image = pygame.transform.scale(bubble_image, (bubble_width, bubble_height))
        bubble_rect = scaled_bubble_image.get_rect(bottomright=(x+bubble_width//4, y))
      self.win.blit(scaled_bubble_image, bubble_rect)

      # Blit the text onto the bubble
      current_y = bubble_rect.top + bubble_padding
      for line in text_lines:
          text_surface = font.render(line, True, (0, 0, 0))
          text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, top=current_y)
          self.win.blit(text_surface, text_rect)
          current_y += text_surface.get_height()


  def emoji_bubble(self, emoji):

    if(self.is_travelling): return

    #eat_emoji = pygame.transform.scale(eat_emoji, EMOJI_SIZE)
    #EMOJI = {'Eat': eat_emoji }

    x = self.x
    y = self.y
    emoji_surface = EMOJI[emoji]

    # Calculate the dimensions of the bubble based on the emoji size
    bubble_padding = 10
    bubble_width = emoji_surface.get_width() + bubble_padding * 2
    bubble_height = emoji_surface.get_height() + bubble_padding * 2
    if(x > 1700):
      bubble_rect = pygame.Rect(x - bubble_width // 2, y - bubble_height // 2 - 30, bubble_width, bubble_height)
    else:
      bubble_rect = pygame.Rect(x + bubble_width // 2 + 30, y - bubble_height // 2 - 30, bubble_width, bubble_height)
    # bubble_rect2 = pygame.Rect(x - bubble_width // 2 - 30, y - bubble_height // 2 - 30, bubble_width, bubble_height)

    # Draw the bubble outline
    outline_width = 3  # Adjust the line width as desired
    pygame.draw.ellipse(self.win, BLACK, bubble_rect, outline_width)
    bubble_rect.inflate_ip(-outline_width, -outline_width)
    # Draw the bubble background
    pygame.draw.ellipse(self.win, WHITE, bubble_rect,0)

    # Blit the emoji onto the bubble
    emoji_rect = emoji_surface.get_rect(centerx=bubble_rect.centerx, top=bubble_rect.top + bubble_padding)
    self.win.blit(emoji_surface, emoji_rect)
