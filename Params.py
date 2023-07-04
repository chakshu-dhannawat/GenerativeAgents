import os

'''
====================
Game
====================
'''

Path = "Assets\\"
Emoji_Path = "Assets\\emojis\\"
WIN_WIDTH = 1150
WIN_HEIGHT = 800
EMOJI_SIZE = (25,25)
FPS = 100

N_Background = sum([len(files) for _, _, files in os.walk('Assets\\Background')])
N_Killing = sum([len(files) for _, _, files in os.walk('Assets\\killing')])
Speed_Killing = 10

FIRE_SIZE = (60,60)
FIRE_CENTER = (855,572)

TavernRadius = 100
TavernCenter = (859,601)

LOCATION_MAP = {'Hut 1':(285,313),#'Hut 1 task01':(148,175),
                'Hut 2':(577,317),#'Hut 2 task01':(471,179),
                #'Hut 3':(414,452),'Hut 3 task01':(317,382),'Hut 3 task02':(433,352),
                'Shrine':(327,743),'Shrine task01':(162,698),'Shrine task02':(228,764),'Shrine task03':(382,764),'Shrine task04':(446,679),
                'Cattle Farm':(859,334),'Cattle Farm task01':(844,256),'Cattle Farm task02':(1127,330),'Cattle Farm task03':(1108,251),'Cattle Farm task04':(1098,444),
                'Well':(556,495),'Well task01':(416,482),'Well task02':(442,533),'Well task03':(528,537),#'Well task04':(494,450),
                'Electricity House':(192,501),#'Electricity House task01':(75,510),'Electricity House task02':(26,438),'Electricity House task03':(64,363),'Electricity House task04':(152,363),
                'Tavern':(791,662),
                'Fishing Pond':(666,69),'Fishing Pond task01':(643,101),'Fishing Pond task02':(742,108),'Fishing Pond task03':(859,118),'Fishing Pond task04':(1036,103),
                'Intermediate01':(660,618),'Intermediate02':(511,618),'Intermediate03':(397,550),'Intermediate04':(287,362),'Intermediate05':(539,357),
                'Intermediate06':(738,374),'Intermediate07':(670,186),#'Intermediate08':(107,75),'Intermediate09':(301,97),'Intermediate10':(849,103),
                }
MESSAGES_MAP = ["Hello!","How are you?",'Anata wa kawaii desu','Watashi wa Takeshi Desu','Hajimemashite','Otsukaresama deshita']

Locations = ['Hut 1','Hut 2','Shrine','Well','Shrine','Shrine']
# InitialPositions = [LOCATION_MAP[loc] for loc in Locations]
InitialPositions = [LOCATION_MAP['Tavern']]*10


'''
====================
Retrieval Alpha
====================
'''

Alpha_Recency = 0.3
Alpha_Importance = 0
Alpha_Relevance = 0.8

'''
====================
Town
====================
'''

townName = "Mk 1 Village"
Initial = "Tavern"

nodes = {"Hut 1": "The first hut",
        "Hut 2": "The second hut",
        #"Hut 3": "The third hut",
        "Well": "A water source providing clean and fresh water for the townfolks",
        "Tavern": "A lively place where townfolks can socialize, exchange information",
        "Electricity House": "generates and distributes electricity power to the town",
        "Cattle Farm": "A dedicated area where livestock is raised for milk, meat, or other dairy products",
        "Fishing Pond": "A designated spot for fishing activities",
        "Shrine": "A sacred place where townfolks can pay homage, meditate, or seek spiritual solace.",
        "Well task01": "Drawing water from the well.",
        "Well task02": "Cleaning the well.",
        "Well task03": "Repairing the pulley system or any damages to the well structure.",
        #"Well task04": "Monitoring the water level and quality of the well.",
        "Cattle Farm task01": "Feeding the animals.",
        "Cattle Farm task02": "Cleaning the animals.",
        "Cattle Farm task03": "Milking the cows and collecting eggs from the chickens.",
        "Cattle Farm task04": "Repairing the fences.",
        #"Electricity House task01": "Maintaining the electricity generator or power source.",
        #"Electricity House task02": "Checking and repairing any electrical equipment or wiring.",
        #"Electricity House task03": "Ensuring a stable power supply to the village.",
        #"Electricity House task04": "Managing the distribution of electrical resources.",
        "Shrine task01": "Offering Rituals",
        "Shrine task02": "Cleaning and Maintenance of the Shrine",
        "Shrine task03": "Lighting Candles at the Shrine",
        "Shrine task04": "Gathering Sacred Herbs",
        # "Hut 1 task01": "Maintaining the cleanliness and tidiness of the houses.",
        # "Hut 2 task01": "Repairing any damages or leaks in the houses.",
        # "Hut 3 task01": "Collecting firewood or fuel for heating and cooking.",
        #"Hut 3 task02": "Checking on elderly or vulnerable villagers, providing assistance if needed.",
        "Fishing Pond task01": "Setting up fishing nets",
        "Fishing Pond task02": "Catching fish",
        "Fishing Pond task03": "Cleaning and preparing the caught fish for cooking.",
        "Fishing Pond task04": "Maintaining the fishing equipment and repairing any damages.",
        "Intermediate01":"Inbetween Nodes",
        "Intermediate02":"Inbetween Nodes",
        "Intermediate03":"Inbetween Nodes",
        "Intermediate04":"Inbetween Nodes",
        "Intermediate05":"Inbetween Nodes",
        "Intermediate06":"Inbetween Nodes",
        "Intermediate07":"Inbetween Nodes",
        #"Intermediate08":"Inbetween Nodes",
        #"Intermediate09":"Inbetween Nodes",
        #"Intermediate10":"Inbetween Nodes",
        }

hubs = [x for x in nodes.keys() if "task" not in x and "Intermediate" not in x]  


'''
====================
Agents
====================
'''

MinDialogues = 8

agentsDetails = [
    {"name": "Yumi Okada", "description": "Yumi is a warewolf; Yumi is smart and is good at lying."},
    {"name": "Yuka Suzuki", "description": "Yuka is a townfolk; Yuka gets easily convinced from other's arguments."},
    {"name": "Riku Mori", "description": "Riku is a townfolk; Riku is smart and has good deduction skills."},
    {"name": "Hina Sato", "description": "Hina is a townfolk; Hina is analytical."},
    {"name": "Mana Yoshida", "description": "Mana is a warewolf; Mana is very smart."},
    {"name": "Taichi Kato", "description": "Taichi is a townfolk; Taichi is dumb."},
    {"name": "Yuria Shimizu", "description": "Yuria is a townfolk; Yuria has good convincing skills."}
]

# agentsDetails = [
#     {"name": "Yumi Okada", "description": "Yumi is a warewolf; Yumi is a highly intelligent and strategic werewolf. With a keen analytical mind and exceptional lying skills, Yumi easily manipulates situations to deceive others."},
#     {"name": "Yuka Suzuki", "description": "Yuka is a townfolk; Yuka is a perceptive and open-minded townfolk. While Yuka tends to get easily convinced by other's arguments, their high IQ allows them to analyze information critically and adapt their perspective accordingly."},
#     {"name": "Riku Mori", "description": "Riku is a townfolk; Riku is a brilliant and observant townfolk. With exceptional deductive reasoning skills and a sharp intellect, Riku excels in analyzing complex situations, making them an asset in identifying the werewolf."},
#     {"name": "Hina Sato", "description": "Hina is a townfolk; Hina is an analytical townfolk who possesses exceptional problem-solving abilities. With their high IQ, Hina carefully evaluates evidence and applies logical thinking to unravel the mysteries of the village."},
#     {"name": "Mana Yoshida", "description": "Mana is a warewolf; Mana is an exceptionally intelligent werewolf with a razor-sharp mind. Their high IQ enables them to devise intricate plans and manipulate others effectively, making it challenging for the townsfolks to identify their true identity."},
#     {"name": "Taichi Kato", "description": "Taichi is a townfolk; Taichi is a townfolk with an astute and intuitive mind. While not conventionally book-smart, Taichi possesses a remarkable talent for pattern recognition and thinking outside the box. Their unique perspective often leads to unconventional yet effective solutions, contributing valuable insights to the discussions and investigations within the village. Taichi's ability to approach problems from different angles and uncover hidden connections showcases their high IQ and intellectual prowess."},
#     {"name": "Yuria Shimizu", "description": "Yuria is a townfolk; Yuria is a charismatic and persuasive townfolk. Yuria's high IQ, combined with excellent convincing skills, allows them to sway others with well-thought-out arguments and logical reasoning."}
# ]


'''
====================
Others
====================
'''

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CREAM = (255,203,164)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
