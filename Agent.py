# This file contains the Agent class which is the main class for the agent
#[このファイルには、エージェントのメインクラスであるエージェントクラスが含まれています。]
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


# Agent initialization with a name, summary, and graphics 
# [名前、概要、グラフィックを含むエージェントの初期化]
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

    # Generating the plan for the day and the strategy for the day based on the summary of the agent 
    # [エージェントのサマリーに基づいて、その日のプランと戦略を作成する。]
    if "werewolf" in summary:
      self.werewolf = True
      QUERY_INIT = QUERY_INIT_WEREWOLF.format(name, name, summary, name, details)
      for player in details.split('\n'):
        self.remember(player.split(') ')[1])
    else: QUERY_INIT = QUERY_INIT_TOWNFOLK.format(name, name, summary, name)
    self.strategy = self.brain.query(QUERY_INIT,name='QUERY_INIT')

    # Log the strategy and the plan for the day
    # [その日の戦略とプランを記録する]
    log(f"{self.name}'s Strategy for {calendar.day} -\n\n{self.strategy}\n\n-----------------------\n\n") 
    
    
    # Start the day with a detailed plan for the day
    # [その日の詳細な計画を立てて1日を始める]
    strategies = extractQuestions(self.strategy)

    for strat in strategies:
      self.remember(strat)

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

    self.walkTimer = random.randint(2000, 3000)  # Random timer between 2000ms and 3000ms [2000ms～3000msのランダムタイマー]
    self.timer = 0
    self.directionTimer = self.walkTimer

    self.folder_name = self.graphics['folder_name']

    self.location_name = self.graphics['initialLocation']
    self.destination=None
    self.destination_x=-10
    self.destination_y=-10
    self.is_travelling = False
    self.destination_path=[]
    
    # Speaking Bubbles [スピーキング・バブル]
    self.isSpeaking = False
    self.msg = None
    self.sleeping = False
    self.sleepSoon = False
    
    self.walkRight, self.walkLeft, self.walkUp, self.walkDown, self.char = self.graphics_load()
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
        except:
          pass
        log(f'{t} : {detailed[t]}')
      self.MinutePlan.update(detailed)
    return self.MinutePlan

  # Retrieving memories from the database and sorting them based on the retrieval score
  # [データベースから記憶を検索し、検索スコアに基づいて並べ替える。]
  def retrieve(self, query, n):
    score = []
    memories_data = DB.getAllMemories(self.name)
    for mem in memories_data:
      score.append(mem.retrievalScore(query))
    ids = sorted(range(len(score)), key=lambda i: score[i], reverse=True)[:n]
    memories = []
    for id in ids:
      memories.append(memories_data[id].observation)
      DB.updateMemories(self.name,memories_data[id]._id,'lastAccess',calendar.dt)
    m = ""
    for i,mem in enumerate(memories): m += f"{i+1}) {mem}\n"
    return memories

  # Reflecting on the memories retrieved and generating insights
  # [検索された記憶を振り返り、洞察を生み出す]
  def reflect(self,n_questions=N_Questions, n_memories=N_Memories, n_reflections=N_Reflections):
    questions = extractQuestions(self.brain.query(QUERY_REFLECT_QUESTIONS.format(getMemories(self.memory),n_questions),remember=False,name='QUERY_REFLECT_QUESTIONS'))
    for question in questions:
      if(question==''): continue
      memories = self.retrieve(question,n_memories)
      insights = extractQuestions(self.brain.query(QUERY_REFLECT_INSIGHTS.format(self.name,getRetrievedMemories(memories),n_reflections),remember=False,name='QUERY_REFLECT_INSIGHTS'))
      for insight in insights:
        if(insight==''): continue
        self.memory.append(Reflection(insight))

  # Generating a random location for the agent to move to
  # [エージェントが移動するランダムな場所の生成]
  def nextLocation(self,now,game):
    try: 
      locationName = self.brain.query(QUERY_LOCATION.format(now,self.name,now,self.plan[timeKey(now)],getHubs(),self.name,self.name),remember=False,name='QUERY_LOCATION')
    except:
      locationName = random.choice(hubs) 
    newLocation = extractHub(locationName)
    
    if(newLocation=="Tavern"): newLocation = random.choice(hubs)
    log(f"\n{self.name} chose to go to {newLocation} at {calendar.time}\n")
    self.remember(f"\n{self.name} chose to go to {newLocation} at {calendar.time}\n")
    self.hub = newLocation
    tasks, tasksList = getTasks(newLocation,game,self.werewolf)
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
    
    try:
      newLocation = tasksList[taskSr-1]
    except:
      newLocation = tasksList[0]

    log(f"\n{self.name} chose to do the task : {newLocation} at {calendar.time}\n")
    self.remember(f"\n{self.name} chose to do the task : {newLocation} at {calendar.time}\n")
    self.dest = "List"
    self.board = True
    self.task = newLocation

  # Loading the graphics for the agent based on movement
  # [移動に基づくエージェントのグラフィックの読み込み]
  def graphics_load(self):
    self.Character_Size = random.choice(Character_Sizes)
    walk_right = []
    walk_left = []
    walk_up = []
    walk_down = []
    temp = None
    folder_path = Path + self.folder_name
    image_files = os.listdir(folder_path)

    # Detect if werewolf or townfolk
    # [狼男か町民かを判断する。]
    if self.werewolf:
      # Load images into walkRight, walkLeft, walkUp, walkDown arrays
      # [画像を walkRight, walkLeft, walkUp, walkDown 配列にロードする。]
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
      # [画像を walkRight, walkLeft, walkUp, walkDown 配列にロードする。]
      for file_name in image_files:
          if file_name.startswith('R'):
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
              temp = pygame.image.load(os.path.join(folder_path, file_name))
              temp = pygame.transform.scale(temp, self.Character_Size)
              walk_down.append(temp)
      self.char_rect = walk_down[0].get_rect() 
      return walk_right, walk_left, walk_up, walk_down, walk_down[0]

  # Drawing the speech bubble [吹き出しを描く]
  def drawBubble(self):
     if(self.sleeping): return
     if self.isSpeaking:
          self.speech_bubble()
  
  # Drawing the agent on the screen and updating the screen [エージェントをスクリーンに描画し、スクリーンを更新する。]
  def draw(self):
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

  # Updating the agent's location and movement    
  # [エージェントの位置と移動の更新]        
  def move(self, VelFactor):
      if(self.sleeping): return
      # If agent has reached location [エージェントが所在地に到着したかどうかの確認]
      if(abs(self.x - self.destination_x)<1+int(self.vel_x) and abs(self.y - self.destination_y)<1+int(self.vel_y)):
          self.left=False
          self.right=False
          self.up=False
          self.down = False
          self.standing=True
          self.location_name = self.destination
          self.is_travelling=False
          
      # Move towards the destination [目的地に向かう]
      if self.is_travelling:
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
          
          # Updation the location of the agent based on the direction of movement
          # [エージェントの位置を移動方向に基づいて更新する。]
          if self.left and self.x > self.vel_x:
              self.x -= self.vel_x
              self.standing = False
          if self.right and self.x < WIN_WIDTH - self.vel_x:
              self.x += self.vel_x
              self.standing = False
          if self.up and self.y > self.vel_y:
              self.y -= self.vel_y
              self.standing = False
          if self.down and self.y < WIN_HEIGHT - self.vel_y:
              self.y += self.vel_y
              self.standing = False
          self.standing = not(self.left or self.right or self.up or self.down)

      else:
          self.timer+=1
          if(self.timer>50):
              self.timer=0
          if len(self.destination_path)==0:
            if(self.board and self.destination=="List"):
               self.board = False 
               self.dest = self.task
            
            if(not self.taskReach and self.destination==self.task): 
              self.taskReach = True
              taskCompleted[self.task] = True

              # Checking if the task is a sabotage task and if it is, then the task is not completed
              # [タスクがサボタージュ・タスクかどうかをチェックし、サボタージュ・タスクであればタスクは完了しない]
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
              pass
              
            elif(self.dest != "Stop" and self.dest != self.destination):
              self.choose_location(self.dest)

            if(self.sleepSoon and self.location_name in SLEEPING_NODES):
              self.sleepSoon = False
              self.sleeping = True

          else:
            self.destination = self.destination_path[0]
            self.destination_path.pop(0)
            
            try:
              self.destination_x, self.destination_y = LOCATION_MAP[self.destination]
            except:
              self.destination_x, self.destination_y = self.destination
            self.is_travelling=True         
              
  # def manual_move(self,keys):

  #     if (keys[pygame.K_a]) and (self.x > self.vel) : 
  #         self.x -= self.vel
  #         self.left = True
  #         self.right = False
  #         self.up=False
  #         self.down=False

  #     if (keys[pygame.K_d]) and (self.x < WIN_WIDTH - self.width - self.vel) : 
  #         self.x += self.vel
  #         self.right = True
  #         self.left = False
  #         self.up=False
  #         self.down=False

  #     if (keys[pygame.K_s]) and (self.y< WIN_WIDTH - self.height - self.vel): 
  #         self.y+= self.vel
  #         self.down = True
  #         self.up=False
  #         self.left=False
  #         self.right=False

  #     if (keys[pygame.K_w]) and (self.y > self.vel + 100) : 
  #         self.y-= self.vel
  #         self.up=  True
  #         self.down=False
  #         self.left=False
  #         self.right=False

  #     self.standing = not (keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d])

  def choose_random_location(self):
      location = random.choice(list(LOCATION_MAP.keys()))
      if(not isinstance(self.location_name, str)): self.location_name = "Tavern"
      self.destination_path = town.shortestPath(self.location_name,location)

  def choose_location(self,location):
      if(not isinstance(self.location_name, str)): self.location_name = "Tavern"
      self.destination_path = town.shortestPath(self.location_name,location)

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

  # Code for the agent to move to a specific location 
  # [エージェントが特定の場所に移動するためのコード]
  def tavern(self,point):
      (x,y) = point
      closest_index = min(range(len(TavernCoordinates)), key=lambda idx: (x - TavernCoordinates[idx][0]) ** 2 + (y - TavernCoordinates[idx][1]) ** 2)
      self.dest = "Stop"
      if(not isinstance(self.location_name, str)): self.location_name = "Tavern"
      self.destination_path = self.destination_path + town.shortestPath(self.location_name,TavernNodes[closest_index])
      self.destination_path.append(point)
  
  def speech_bubble(self):
      text = self.msg
      x = self.x
      y = self.y
      bubble_image = pygame.image.load(Path+"speechbubble_png_blue.png")  
      bubble_image2 = pygame.image.load(Path+"onevoneelectricspeechbubble.png")
      font_size = 22
      font = pygame.font.Font(None, font_size)
      words = text.split()
      text_lines = []
      line = ""
      for word in words:
          if len(line.split()) < CONVERSATION_WORD_LIMIT:
              line += " " + word
          else:
              text_lines.append(line.strip())
              line = word
      text_lines.append(line.strip())
      max_width = 0
      total_height = 0
      for line in text_lines:
          text_surface = font.render(line, True, (0, 0, 0))
          max_width = max(max_width, text_surface.get_width())
          total_height += text_surface.get_height()

      # Create the bubble rectangle around the text
      # [テキストの周囲にバブル矩形を作成する]
      bubble_padding = 20
      bubble_width = max_width + bubble_padding * 10
      bubble_height = total_height + bubble_padding * 4

      # Blit the bubble image onto the surface
      # [表面に泡のイメージ]
      if(x<200):
        scaled_bubble_image = pygame.transform.scale(bubble_image2, (bubble_width, bubble_height))
        bubble_rect = scaled_bubble_image.get_rect(bottomleft=(x-bubble_width//4, y))
      else:
        scaled_bubble_image = pygame.transform.scale(bubble_image, (bubble_width, bubble_height))
        bubble_rect = scaled_bubble_image.get_rect(bottomright=(x+bubble_width//4, y))
      self.win.blit(scaled_bubble_image, bubble_rect)

      # Blit the text onto the bubble
      # [テキストをバブルに]
      current_y = bubble_rect.top + bubble_padding
      for line in text_lines:
          text_surface = font.render(line, True, (0, 0, 0))
          text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, top=current_y)
          self.win.blit(text_surface, text_rect)
          current_y += text_surface.get_height()

  # Emoji Bubbles for showing tasks
  # [タスクを示す絵文字バブル]
  def emoji_bubble(self, emoji):

    if(self.is_travelling): 
      return
    x = self.x
    y = self.y
    emoji_surface = EMOJI[emoji]

    # Calculating the dimensions of the bubble based on the emoji size
    # [絵文字のサイズに基づいてバブルの寸法を計算する]
    bubble_padding = 10
    bubble_width = emoji_surface.get_width() + bubble_padding * 2
    bubble_height = emoji_surface.get_height() + bubble_padding * 2
    if(x > 1700):
      bubble_rect = pygame.Rect(x - bubble_width // 2, y - bubble_height // 2 - 30, bubble_width, bubble_height)
    else:
      bubble_rect = pygame.Rect(x + bubble_width // 2 + 30, y - bubble_height // 2 - 30, bubble_width, bubble_height)

    # Draw the bubble outline [バブルの輪郭を描く]
    outline_width = 3  # Adjust the line width as desired [線幅を調整する]
    pygame.draw.ellipse(self.win, BLACK, bubble_rect, outline_width)
    bubble_rect.inflate_ip(-outline_width, -outline_width)

    # Draw the bubble background [バブルの背景を描く]
    pygame.draw.ellipse(self.win, WHITE, bubble_rect,0)
    
    # Blit the emoji onto the bubble [絵文字をバブルに乗せる]
    emoji_rect = emoji_surface.get_rect(centerx=bubble_rect.centerx, top=bubble_rect.top + bubble_padding)
    self.win.blit(emoji_surface, emoji_rect)
