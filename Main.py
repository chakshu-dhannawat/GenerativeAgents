# This file is the main file of the game. It contains the main loop of the game and the game logic.
# [このファイルはゲームのメインファイルです。ゲームのメインループとゲームロジックが含まれています。]

from Agent import Agent  
from Game import Game 
from Params import *
from Util import log
from datetime import datetime as dt
import threading
import time
from queue import Queue
from HoveringBox import *
from pygame.locals import *
from Game_start import Game_start

try: 
  with open("Logs/logs.txt", 'w') as file: pass
except:
  os.makedirs("Logs", exist_ok=True)
log("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
log(dt.now().strftime("%m/%d/%Y, %H:%M:%S"))

'''
====================
Initializing Agents [エージェントの初期化]
====================
'''
log('\n=======Initializing Agents=======\n')

graphics = [{'x':InitialPositions[i][0],'y':InitialPositions[i][1],'width':64, 'height':64, 'folder_name': f'character_0{i+1}', 'initialLocation': "Tavern"} for i in range(len(agentsDetails))] 

class getAgents():   
  def __init__(self):
    self.agents = [None]*len(agentsDetails)

  # Create the agents [エージェントの作成]
  def makeAgent(self,i):
    self.agents[i] = Agent(agentsDetails[i]['name'],agentsDetails[i]['description'],graphics[i])
    agentMap[agentsDetails[i]['name']] = self.agents[i]

  # Create the threads for each agent [各エージェントのスレッドを作成する]
  def get(self):
    threads = []
    for i in range(len(agentsDetails)):
        thread = threading.Thread(target=self.makeAgent, args=(i,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()  
    return self.agents 

agents = getAgents().get()
if(None in agents):
  agents = [Agent(agent['name'],agent['description'],graphics[i]) for i,agent in enumerate(agentsDetails)]

'''
====================
Initializing Game [ゲームの初期化]
====================
'''
log('\n=======Initializing Game=======\n')

game = Game(agents)



'''
====================
Game Start Button [試合開始ボタン]
====================
'''

game_start = Game_start(game.win)
game_start.start()

'''
====================
Werewolf Game [LOGIC] [人狼ゲーム[ロジック]]
====================
'''
log('\n=======Werewolf Game=======\n')

def game_logic():  
  time.sleep(1)
  day = 2

  while game.run:
     
    if(day<2): 
      game.switchPhase()

    if(day==0): 
      log('\n======= Night Phase =======\n') 
      game.nightVote()
    if(day==1): 
      log('\n======= Morning Voting Phase =======\n')
      game.dayVote()
    if(day==2): 
      log('\n======= Day Tasks Phase =======\n')
      game.afternoon()
    
    day = (day+1)%3


'''
====================
Werewolf Game [GRAPHICS] [人狼ゲーム [GRAPHICS]]
====================
'''

def render():
  while game.run : 
      game.clock.tick(FPS)
      game.step()

'''
====================
Running Game using Multi-Threading [マルチスレッドによるゲームの実行]
====================
'''

logic_thread = threading.Thread(target=game_logic)
logic_thread.start()

if __name__ == '__main__':

  render()

