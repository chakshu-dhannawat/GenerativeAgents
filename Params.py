# This file contains all the parameters used in the game. [このファイルには、ゲームで使用されるすべてのパラメータが含まれています。]

import os
import time
import random
import pygame
from HoveringBox import HoverTextBox


'''
====================
Agents [代理店]
====================
'''
agentMap = {}
MinDialogues = 5
MaxDialogues = 8

N_Questions=3
N_Memories=5
N_Reflections=5

# --------------------------------Agent names descriptions for the game with varying IQ levels [IQレベルが異なるゲームのエージェント名の説明]--------------------------------

# Different IQ [IQの違い]
agentsDetails = [
    {"name": "Yumi Okada", "description": "Yumi is a werewolf; Yumi is smart, good at lying, and a farmer who works in the Cattle Farm. Also, Yumi tries to sabotage the tasks of the townfolks."},
    {"name": "Yuka Suzuki", "description": "Yuka is a townfolk; Yuka gets easily convinced by others' arguments and takes care of the well and its maintenance."},
    {"name": "Riku Mori", "description": "Riku is a townfolk; Riku is smart, has good deduction skills, and loves fishing in the Fishing area."},
    {"name": "Hina Sato", "description": "Hina is a townfolk; Hina is analytical and is a monk who works in the Shrine."},
    {"name": "Mana Yoshida", "description": "Mana is a werewolf; Mana is brilliant and an electrician who works in the Electricity House. Also, Mana tries to sabotage the tasks of the townfolks."},
    {"name": "Taichi Kato", "description": "Taichi is a townfolk and an electrician who does tasks at the Electricity House; Taichi is dumb."},
    {"name": "Yuria Shimizu", "description": "Yuria is a townfolk; Yuria has good convincing skills and is a farmer who works in the Cattle Farm."},
    {"name": "Haruka Itō", "description": "Haruka is a townfolk; Haruka has low convincing skills and is a fisherperson who works in the Fishing area. Haruka is friendly and loves talking"}
]

# Same IQ - High IQ (7-8) [同じIQ - 高いIQ (7-8)]
# agentsDetails = [
#     {"name": "Yumi Okada", "description": "Yumi is a werewolf; Yumi is a highly intelligent and strategic werewolf. With a keen analytical mind and exceptional lying skills, Yumi easily manipulates situations to deceive others."},
#     {"name": "Yuka Suzuki", "description": "Yuka is a townfolk; Yuka is a perceptive and open-minded townfolk. While Yuka tends to get easily convinced by other's arguments, their high IQ allows them to analyze information critically and adapt their perspective accordingly."},
#     {"name": "Riku Mori", "description": "Riku is a townfolk; Riku is a brilliant and observant townfolk. With exceptional deductive reasoning skills and a sharp intellect, Riku excels in analyzing complex situations, making them an asset in identifying the werewolf."},
#     {"name": "Hina Sato", "description": "Hina is a townfolk; Hina is an analytical townfolk who possesses exceptional problem-solving abilities. With their high IQ, Hina carefully evaluates evidence and applies logical thinking to unravel the mysteries of the village."},
#     {"name": "Mana Yoshida", "description": "Mana is a werewolf; Mana is an exceptionally intelligent werewolf with a razor-sharp mind. Their high IQ enables them to devise intricate plans and manipulate others effectively, making it challenging for the townsfolks to identify their true identity."},
#     {"name": "Taichi Kato", "description": "Taichi is a townfolk; Taichi is a townfolk with an astute and intuitive mind. While not conventionally book-smart, Taichi possesses a remarkable talent for pattern recognition and thinking outside the box. Their unique perspective often leads to unconventional yet effective solutions, contributing valuable insights to the discussions and investigations within the village. Taichi's ability to approach problems from different angles and uncover hidden connections showcases their high IQ and intellectual prowess."},
#     {"name": "Yuria Shimizu", "description": "Yuria is a townfolk; Yuria is a charismatic and persuasive townfolk. Yuria's high IQ, combined with excellent convincing skills, allows them to sway others with well-thought-out arguments and logical reasoning."}
# ]

# Same IQ - Low IQ (3-4) [同じIQ - 低IQ (3-4)]
# agentsDetails = [
#     {"name": "Yumi Okada", "description": "Yumi is an average-intelligence werewolf. While not exceptionally smart, Yumi relies on their instincts and basic deception skills to survive in the game."},
#     {"name": "Yuka Suzuki", "description": "Yuka is an average-intelligence townfolk who tends to go along with the majority. Their analytical skills are moderate, and they try their best to contribute to the discussions based on the information available."},
#     {"name": "Riku Mori", "description": "Riku is an average-intelligence townfolk with limited deductive reasoning skills. They rely more on intuition and observations rather than advanced analytical thinking."},
#     {"name": "Hina Sato", "description": "Hina is an average-intelligence townfolk who approaches situations with a practical mindset. While not highly analytical, Hina tries to make logical decisions based on common sense."},
#     {"name": "Mana Yoshida", "description": "Mana is an average-intelligence werewolf who relies on basic strategies and manipulation tactics. While not highly intelligent, Mana can blend in with the townfolks and create confusion during discussions."},
#     {"name": "Taichi Kato", "description": "Taichi is an average-intelligence townfolk who sometimes struggles to grasp complex information. Their contributions may be simple and straightforward, but they genuinely try to participate and support the town's decision-making process."},
#     {"name": "Yuria Shimizu", "description": "Yuria is an average-intelligence townfolk with decent persuasive skills. They can present their ideas convincingly but may not excel in complex problem-solving or critical thinking."}
# ]

'''
====================
Game [ゲーム]
====================
'''

Path = "Assets/"
Emoji_Path = "Assets/emojis/"
WIN_WIDTH = 1920
WIN_HEIGHT = 1080
DEFAULT_IMAGE_SIZE = (WIN_WIDTH, WIN_HEIGHT)
FPS = 60
Clock_Speed = 60
Character_Speed = 1.25


HOUSE_POPUP_SIZE = (1024,748)
HOVER_WORD_LIMIT = 8
CONVERSATION_WORD_LIMIT = 6
POPUP_BUTTON_SIZE = (35,35)

transcript_rect_width, transcript_rect_height = 400, 600

HUT1_POPUP_CLOSE = (976, 19)
HUT2_POPUP_CLOSE = ()

N_Background = sum([len(files) for _, _, files in os.walk('Assets/Background')])
N_Killing = sum([len(files) for _, _, files in os.walk('Assets/killing')])
N_Farewell_T = sum([len(files) for _, _, files in os.walk('Assets/Farewell/Townfolk')])
N_Farewell_W = sum([len(files) for _, _, files in os.walk('Assets/Farewell/Werewolf')])
Speed_Killing = FPS//10

EMOJI_SIZE = (58, 47)
FIRE_SIZE = (100, 81)
FIRE_CENTER = (1427, 772)
TavernCenter = (1434, 811)
Character_Sizes = [(random.randint(55, 66), random.randint(44, 54)) for _ in range(len(agentsDetails))]
TavernRadius = 150

SLEEPING_NODES = ['Hut 1 Sleeping01', 'Hut 1 Sleeping02', 'Hut 1 Sleeping03', 'Hut 1 Sleeping04','Hut 2 Sleeping01', 'Hut 2 Sleeping02', 'Hut 2 Sleeping03', 'Hut 2 Sleeping04']

# Location of the nodes for agent movement [エージェント移動用ノードの位置]
LOCATION_MAP = {'Hut 1': (475, 422), "Hut 1 Main": (135, 376), 
                "Hut 1 Intermediate01":(305, 336), "Hut 1 Intermediate02":(324, 245), "Hut 1 Intermediate03":(324, 157),"Hut 1 Intermediate04":(509, 336),"Hut 1 Intermediate05":(686, 336), "Hut 1 Intermediate06":(142, 464), "Hut 1 Intermediate07":(225,541),
                "Hut 1 task01":(217,127), "Hut 1 task04":(287,542),"Hut 1 SleepIntermediate01":(478,282), "Hut 1 SleepIntermediate02":(678,280), "Hut 1 SleepIntermediate03":(712,142), "Hut 1 SleepIntermediate04":(862,245), "Hut 1 SleepIntermediate05":(929,222),
                "Hut 1 Sleeping01":(590,118), "Hut 1 Sleeping02":(766, 121), "Hut 1 Sleeping03":(820, 120), "Hut 1 Sleeping04":(862, 124), #"Hut 1 Sleeping05":(616,198),
                'Hut 2': (963, 427), "Hut 2 Main": (623, 381),
                "Hut 2 Intermediate01": (793, 371), "Hut 2 Intermediate02": (812, 250), "Hut 2 Intermediate03": (812, 162), "Hut 2 Intermediate04": (997, 371), "Hut 2 Intermediate05": (1174, 371), "Hut 2 Intermediate06": (630, 469), "Hut 2 Intermediate07": (713, 546),
                "Hut 2 task01": (670, 130), "Hut 2 task04": (780, 547), "Hut 2 SleepIntermediate01":(936,287), "Hut 2 SleepIntermediate02":(1136,285), "Hut 2 SleepIntermediate03":(1170,147), "Hut 2 SleepIntermediate04":(1320,250), "Hut 2 SleepIntermediate05":(1387,227),
                "Hut 2 Sleeping01":(1048,123), "Hut 2 Sleeping02":(1224, 126), "Hut 2 Sleeping03":(1278, 125), "Hut 2 Sleeping04":(1320, 129), #"Hut 2 Sleeping05": (1104, 203),
                'Shrine': (545, 992), 'Shrine task01': (270, 942), 'Shrine task02': (380, 1012), 'Shrine task03': (637, 1019), 'Shrine task04': (744, 916),
                'Cattle Farm': (1434, 450), 'Cattle Farm task01': (1409, 345), 'Cattle Farm task02': (1881, 445), 'Cattle Farm task03': (1849, 338), 'Cattle Farm task04': (1833, 599), 
                'Well': (928, 668), 'Well task01': (694, 650), 'Well task02': (737, 719), 'Well task03': (881, 724), 
                'Electricity House': (320, 676), 'Electricity House task01': (322, 750),  'Electricity House task02': (264,802),  'Electricity House task03': (173,775),  'Electricity House task04': (100,777), 
                'Tavern': (1320, 893), 
                'Predetermined 01': (1325, 816), 'Predetermined 02': (1389, 737), 'Predetermined 03': (1557, 718), 'Predetermined 04': (1654, 823), 'Predetermined 05': (1589, 947), 'Predetermined 06': (1407, 958), 
                'Fishing Pond': (1111, 93), 'Fishing Pond task01': (1073, 136), 'Fishing Pond task02': (1238, 145), 'Fishing Pond task03': (1434, 159), 'Fishing Pond task04': (1729, 139), 
                'Intermediate01': (1101, 834), 'Intermediate02': (853, 834), 'Intermediate03': (662, 742), 'Intermediate04': (479, 488) , 'Intermediate05': (899, 481), 'Intermediate06': (1232, 504), 'Intermediate07': (1118, 251), 'Intermediate08': (475,425), 'Intermediate09': (963,430), 
                'List':(900, 900)
                }

# Message Map for the agents [エージェント用メッセージマップ]
MESSAGES_MAP = ["Hello!","How are you?",'Anata wa kawaii desu','Watashi wa Takeshi Desu','Hajimemashite','Otsukaresama deshita']

Locations = ['Hut 1','Hut 2','Shrine','Well','Shrine','Shrine']


TavernNodes = [key for key in LOCATION_MAP.keys() if 'Predetermined' in key]
TavernNodes.append('Tavern')
TavernCoordinates = [LOCATION_MAP[key] for key in TavernNodes]

TasksWin = 15
TasksBarWidth = int(WIN_WIDTH*0.4)
TasksBarHeight = 40
TaskBarX = (WIN_WIDTH-TasksBarWidth)//2
TaskBarY = 25


'''
====================
Retrieval Alpha [リトリーバル・アルファ]
====================
'''

Alpha_Recency = 0.2
Alpha_Importance = 0
Alpha_Relevance = 0.8

'''
====================
Town [タウン]
====================
'''

townName = "Mk 1 Village"
Initial = "Well"
InitialPositions = ["Tavern","Well","Shrine","Fishing Pond","Electricity House","Cattle Farm","Tavern","Well","Shrine","Fishing Pond"]
InitialPositions = [LOCATION_MAP[pos] for pos in InitialPositions]

nodes = {"Hut 1": "The first hut.",
        "Hut 1 Main": "Connection between inside and outside of house",
        "Hut 1 Intermediate01":"Inbetween Nodes",
        "Hut 1 Intermediate02":"Inbetween Nodes",
        "Hut 1 Intermediate03":"Inbetween Nodes",
        "Hut 1 Intermediate04":"Inbetween Nodes",
        "Hut 1 Intermediate05":"Inbetween Nodes",
        "Hut 1 Intermediate06":"Inbetween Nodes",
        "Hut 1 Intermediate07":"Inbetween Nodes",
        "Hut 1 Sleeping01":"Sleeping Node",
        "Hut 1 Sleeping02":"Sleeping Node",
        "Hut 1 Sleeping03":"Sleeping Node",
        "Hut 1 Sleeping04":"Sleeping Node",
        "Hut 1 task01": "Reading Books.",
        "Hut 1 SleepIntermediate01": "Sleeping Intermediate",
        "Hut 1 SleepIntermediate02": "Sleeping Intermediate",
        "Hut 1 SleepIntermediate03": "Sleeping Intermediate",
        "Hut 1 SleepIntermediate04": "Sleeping Intermediate",
        "Hut 1 SleepIntermediate05": "Sleeping Intermediate",
        "Hut 1 task04": "Cooking.",
        "Hut 2": "The second hut.",
        "Hut 2 Main": "Connection between inside and outside of house",
        "Hut 2 Intermediate01": "Inbetween Nodes",
        "Hut 2 Intermediate02": "Inbetween Nodes",
        "Hut 2 Intermediate03": "Inbetween Nodes",
        "Hut 2 Intermediate04": "Inbetween Nodes",
        "Hut 2 Intermediate05": "Inbetween Nodes",
        "Hut 2 Intermediate06": "Inbetween Nodes",
        "Hut 2 Intermediate07": "Inbetween Nodes",
        "Hut 2 task01": "Reading Books.",
        "Hut 2 SleepIntermediate01": "Sleeping Intermediate",
        "Hut 2 SleepIntermediate02": "Sleeping Intermediate",
        "Hut 2 SleepIntermediate03": "Sleeping Intermediate",
        "Hut 2 SleepIntermediate04": "Sleeping Intermediate",
        "Hut 2 SleepIntermediate05": "Sleeping Intermediate",
        "Hut 2 Sleeping01":"Sleeping Node",
        "Hut 2 Sleeping02":"Sleeping Node",
        "Hut 2 Sleeping03":"Sleeping Node",
        "Hut 2 Sleeping04":"Sleeping Node",
        "Hut 2 task04": "Cooking.",
        "Well": "A water source providing clean and fresh water for the townfolks.",
        "Tavern": "A lively place where townfolks can socialize, exchange information.",
        "Electricity House": "generates and distributes electricity power to the town.",
        "Electricity House task01": "Maintaining the electricity generator or power source.",
        "Electricity House task02": "Checking and repairing any electrical equipment or wiring.",
        "Electricity House task03": "Managing the distribution of electrical resources.",
        "Electricity House task04": "Managing the distribution of electrical resources.",
        "Cattle Farm": "A dedicated area where livestock is raised for milk, meat, or other dairy products.",
        "Fishing Pond": "A designated spot for fishing activities.",
        "Shrine": "A sacred place where townfolks can pay homage, meditate, or seek spiritual solace.",
        "Well task01": "Drawing water from the well.",
        "Well task02": "Cleaning the well.",
        "Well task03": "Doing hole in the bucket.",
        "Cattle Farm task01": "Feeding the animals.",
        "Cattle Farm task02": "Breaking the fences.",
        "Cattle Farm task03": "Milking the cows and collecting eggs from the chickens.",
        "Cattle Farm task04": "Repairing the fences.",
        "Shrine task01": "Offering Rituals.",
        "Shrine task02": "Cleaning and Maintenance of the Shrine.",
        "Shrine task03": "Lighting Candles at the Shrine.",
        "Shrine task04": "Break the broomstick.",
        "Fishing Pond task01": "Breaking the Fishing Rod.",
        "Fishing Pond task02": "Catching fish.",
        "Fishing Pond task03": "Cleaning and preparing the caught fish for cooking.",
        "Fishing Pond task04": "Maintaining the fishing equipment and repairing any damages.",
        "Intermediate01":"Inbetween Nodes",
        "Intermediate02":"Inbetween Nodes",
        "Intermediate03":"Inbetween Nodes",
        "Intermediate04":"Inbetween Nodes",
        "Intermediate05":"Inbetween Nodes",
        "Intermediate06":"Inbetween Nodes",
        "Intermediate07":"Inbetween Nodes",
        "Intermediate08":"Inbetween Nodes",
        "Intermediate09":"Inbetween Nodes",
        "Predetermined 01":"Pre determined inbetween Nodes",
        "Predetermined 02":"Pre determined inbetween Nodes",
        "Predetermined 03":"Pre determined inbetween Nodes",
        "Predetermined 04":"Pre determined inbetween Nodes",
        "Predetermined 05":"Pre determined inbetween Nodes",
        "Predetermined 06":"Pre determined inbetween Nodes",
        "List": "Agents write their daily activity here."

        }

# Boolean to check if the task is completed [タスクが完了したかどうかをチェックするブール値]
taskCompleted = {"Well task01": False, "Well task02": False, "Well task03": False,
                "Cattle Farm task01": False, "Cattle Farm task02": False, "Cattle Farm task03": False, "Cattle Farm task04": False,
                "Shrine task01": False, "Shrine task02": False, "Shrine task03": False, "Shrine task04": False,
                "Hut 1 task01": False, "Hut 1 task04": False,
                "Hut 2 task01": False, "Hut 2 task04": False,
                "Hut 3 task01": False, "Hut 3 task04": False,
                "Electricity House task01": False,"Electricity House task02": False,"Electricity House task03": False,"Electricity House task04": False,
                "Fishing Pond task01": False, "Fishing Pond task02": False, "Fishing Pond task03": False, "Fishing Pond task04": False
                }

hubs = ["Well","Cattle Farm","Shrine","Fishing Pond","Hut 1","Hut 2","Electricity House"]

'''
====================
Emoji [絵文字]
====================
'''


TASK_EMOJI_MAP = {
    'Well task01': 'Bucket',
    'Well task02': 'Broom',
    'Well task03': 'Bucket_Sabotage',
    'Cattle Farm task01': 'Cow',
    'Cattle Farm task02': 'Fence_Sabotage',
    'Cattle Farm task03': 'Eggs',
    'Cattle Farm task04': 'Wood',
    'Shrine task01': 'Prayer',
    'Shrine task02': 'Broom',
    'Shrine task03': 'Lamp',
    'Shrine task04': 'Broom_Sabotage',
    'Fishing Pond task01': 'FishingPole_Sabotage',
    'Fishing Pond task02': 'Fish',
    'Fishing Pond task03': 'Fishing Pole',
    'Fishing Pond task04': 'Wood',
    "Hut 1 task01": "Reading_Books",
    "Hut 1 Sleeping01": "Sleeping",
    "Hut 1 Sleeping02": "Sleeping",
    "Hut 1 Sleeping03": "Sleeping",
    "Hut 1 Sleeping04": "Sleeping",
    "Hut 2 Sleeping01": "Sleeping",
    "Hut 2 Sleeping02": "Sleeping",
    "Hut 2 Sleeping03": "Sleeping",
    "Hut 2 Sleeping04": "Sleeping",
    "Hut 1 task04": "Cooking",
    "Hut 2 task01": "Reading_Books",
    "Hut 2 task04": "Cooking",
    "Electricity House task01":'Electric Maintain',
    "Electricity House task02":'Electric Repairing',
    "Electricity House task03":'Electric Resources',
    "Electricity House task04":'Electric_Sabotage',
    
}


'''
====================
Others [その他]
====================
'''

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CREAM = (255,203,164)
RED = (255, 0, 0)
DARK_RED = (179,25,25,255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

'''
====================
Hovering Text Box [GRAPHIC]  [ホバリング・テキスト・ボックス[グラフィック］]
====================
'''
pygame.font.init()
font = pygame.font.Font(None, 24)

# Shrine [神社]
shrine_rect = pygame.Rect(386, 728, 200, 200)
shrine_hover_textbox = HoverTextBox(shrine_rect, font, (255, 255, 255), (0, 0, 255), 'Shrine', nodes['Shrine'], f"Available Tasks: {nodes['Shrine task01']}{nodes['Shrine task02']}{nodes['Shrine task03']}{nodes['Shrine task04']}")

# Electricity House [電気ハウス]
electricity_house_rect = pygame.Rect(67, 514, 200, 120)
electricity_house_hover_textbox = HoverTextBox(electricity_house_rect, font, (255, 255, 255), (0, 0, 255), 'Electricity House', nodes['Electricity House'], f"Available Tasks: {nodes['Electricity House task01']}{nodes['Electricity House task02']}{nodes['Electricity House task03']}")

# House 1 [ハウス1]
house1_rect = pygame.Rect(187, 156, 250, 200)
house1_hover_textbox = HoverTextBox(house1_rect, font, (255, 255, 255), (0, 0, 255), 'Hut 1', nodes['Hut 1'], f"Available Tasks: {nodes['Hut 1 task01']}{nodes['Hut 1 task04']}")

# House 2 [ハウス2]
house2_rect = pygame.Rect(662, 167, 250, 200)
house2_hover_textbox = HoverTextBox(house2_rect, font, (255, 255, 255), (0, 0, 255), 'Hut 2', nodes['Hut 2'], f"Available Tasks: {nodes['Hut 2 task01']}{nodes['Hut 2 task04']}")

# Fishing Pond [釣り堀]
fishing_pond_rect = pygame.Rect(1000, 50, 400, 60)
fishing_pond_hover_textbox = HoverTextBox(fishing_pond_rect, font, (255, 255, 255), (0, 0, 255), 'Fishing Pond', nodes['Fishing Pond'], f"Available Tasks: {nodes['Fishing Pond task01']}{nodes['Fishing Pond task02']}{nodes['Fishing Pond task03']}{nodes['Fishing Pond task04']}")

# Cattle Farm [牧場]
cattle_farm_rect = pygame.Rect(1600, 347, 200, 200)
cattle_farm_hover_textbox = HoverTextBox(cattle_farm_rect, font, (255, 255, 255), (0, 0, 255), 'Cattle Farm', nodes['Cattle Farm'], f"Available Tasks: {nodes['Cattle Farm task01']}{nodes['Cattle Farm task02']}{nodes['Cattle Farm task03']}{nodes['Cattle Farm task04']}")

# Tavern [共用集会スペース]
tavern_rect = pygame.Rect(1413, 723, 200, 200)
tavern_hover_textbox = HoverTextBox(tavern_rect, font, (255, 255, 255), (0, 0, 255), 'Tavern', nodes['Tavern'], "")

# Well [良い]
well_rect = pygame.Rect(774, 487, 100, 100)
well_hover_textbox = HoverTextBox(well_rect, font, (255, 255, 255), (0, 0, 255), 'Well', nodes['Well'], f"Available Tasks: {nodes['Well task01']}{nodes['Well task02']}{nodes['Well task03']}")


hover_dict = {
    'Shrine': shrine_hover_textbox,
    'Electricity House': electricity_house_hover_textbox,
    'Hut 1': house1_hover_textbox,
    'Hut 2': house2_hover_textbox,
    'Fishing Pond': fishing_pond_hover_textbox,
    'Cattle Farm': cattle_farm_hover_textbox,
    'Tavern': tavern_hover_textbox,
    'Well': well_hover_textbox
}

# Making pdf of the logs [過去ログのPDF化]
PDF_Name = time.strftime("Logs/%Y-%m-%d %H-%M-%S.pdf", time.localtime(time.time()))
