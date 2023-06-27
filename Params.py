'''
====================
Game
====================
'''

Path = "Assets\\"

WIN_WIDTH = 1000
WIN_HEIGHT = 700

FPS = 100

TavernRadius = 100

LOCATION_MAP = {'Hut 1':(140,180),'Hut 1 task01':(141,246),
                'Hut 2':(435,210),'Hut 2 task01':(368,159),
                'Hut 3':(369,390),'Hut 3 task01':(426,349),'Hut 3 task02':(336,436),
                'Shrine':(285,610),'Shrine task01':(370,557),'Shrine task02':(200,526),'Shrine task03':(376,658),'Shrine task04':(148,602),
                'Cattle Farm':(867,254),'Cattle Farm task01':(781,327),'Cattle Farm task02':(917,310),'Cattle Farm task03':(914,152),'Cattle Farm task04':(759,168),
                'Well':(534,452),'Well task01':(446,497),'Well task02':(494,529),'Well task03':(548,513),'Well task04':(458,465),
                'Electricity House':(117,439),'Electricity House task01':(34,478),'Electricity House task02':(77,357),'Electricity House task03':(190,427),'Electricity House task04':(184,477),
                'Tavern':(810,550),
                'Fishing Pond':(576,80),'Fishing Pond task01':(262,100),'Fishing Pond task02':(111,100),'Fishing Pond task03':(637,100),'Fishing Pond task04':(927,100),
                }
MESSAGES_MAP = ["Hello!","How are you?",'Anata wa kawaii desu','Watashi wa Takeshi Desu','Hajimemashite','Otsukaresama deshita']

Locations = ['Hut 1','Hut 2','Hut 3','Shrine','Well','Shrine','Shrine']
InitialPositions = [LOCATION_MAP[loc] for loc in Locations]


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
        "Hut 3": "The third hut",
        "Well": "A water source providing clean and fresh water for the townfolks",
        "Tavern": "A lively place where townfolks can socialize, exchange information",
        "Electricity House": "generates and distributes electricity power to the town",
        "Cattle Farm": "A dedicated area where livestock is raised for milk, meat, or other dairy products",
        "Fishing Pond": "A designated spot for fishing activities",
        "Shrine": "A sacred place where townfolks can pay homage, meditate, or seek spiritual solace.",
        "Well task01": "Drawing water from the well and distributing it to the villagers.",
        "Well task02": "Ensuring the well is clean and free from any contamination.",
        "Well task03": "Repairing the pulley system or any damages to the well structure.",
        "Well task04": "Monitoring the water level and quality of the well.",
        "Cattle Farm task01": "Feeding the animals and ensuring they have enough water.",
        "Cattle Farm task02": "Cleaning the animal pens and maintaining their hygiene.",
        "Cattle Farm task03": "Milking the cows and collecting eggs from the chickens.",
        "Cattle Farm task04": "Repairing or maintaining the fences and structures in the farm.",
        "Electricity House task01": "Maintaining the electricity generator or power source.",
        "Electricity House task02": "Checking and repairing any electrical equipment or wiring.",
        "Electricity House task03": "Ensuring a stable power supply to the village.",
        "Electricity House task04": "Managing the distribution of electrical resources.",
        "Shrine task01": "Offering Rituals: Agents can perform regular rituals and offer prayers at the Shrine to seek divine guidance and protection for the village.",
        "Shrine task02": "Cleaning and Maintenance: Agents can ensure that the Shrine area is clean and well-maintained, including sweeping, removing debris, and maintaining the altar or sacred objects.",
        "Shrine task03": "Lighting and Incense: Agents can light candles or oil lamps and burn incense at the Shrine, creating a peaceful and spiritual atmosphere.",
        "Shrine task04": "Gathering Sacred Herbs: Agents can search for and gather specific herbs or flowers near the Shrine that are used for religious rituals or medicinal purposes.",
        "Hut 1 task01": "Maintaining the cleanliness and tidiness of the houses.",
        "Hut 2 task01": "Repairing any damages or leaks in the houses.",
        "Hut 3 task01": "Collecting firewood or fuel for heating and cooking.",
        "Hut 3 task02": "Checking on elderly or vulnerable villagers, providing assistance if needed.",
        "Fishing Pond task01": "Setting up and checking fishing nets or traps.",
        "Fishing Pond task02": "Casting lines and catching fish for the village's food supply.",
        "Fishing Pond task03": "Cleaning and preparing the caught fish for cooking.",
        "Fishing Pond task04": "Maintaining the fishing equipment and repairing any damages."
        }


'''
====================
Agents
====================
'''

MinDialogues = 5

agentsDetails = [
    {"name": "Takeshi Yamamoto", "description": "Takeshi is a warewolf; Takeshi is smart and is good at lying."},
    {"name": "Hiroshi Tanaka", "description": "Hiroshi is a townfolk; Hiroshi gets easily convinced from other's arguments."},
    {"name": "Aya Suzuki", "description": "Aya is a townfolk; Aya is smart and has good deduction skills."},
    # {"name": "Sakura Kobayashi", "description": "Sakura is a townfolk; Sakura is analytical."},
    # {"name": "Yumi Kimura", "description": "Yumi is a warewolf; Yumi is very smart."},
    # {"name": "Kaito Sato", "description": "Kaito is a townfolk; Kaito is dumb."},
    # {"name": "Akiko Tanaka", "description": "Akiko is a townfolk; Akiko has good convincing skills."}
]


'''
====================
Others
====================
'''

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CREAM = (255,203,164)