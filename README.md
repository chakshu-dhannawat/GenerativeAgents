# GenerativeAgents - Werewolves of Miller's Hollow

"Werewolves of Miller's Hollow" is a popular social deduction game where players are assigned roles as townfolks, werewolves, or special characters, and the goal is to either eliminate all the werewolves or have the werewolves outnumber the villagers or complete all the assigned tasks. 

During the game, players participate in a series of day and night phases. During the night, the werewolves choose a villager to eliminate, and certain special characters may perform their unique abilities. During the day, the surviving players discuss and vote on who they believe is a werewolf. The player with the most votes is "lynched" and removed from the game. 

The game continues with alternating day and night phases until either all the werewolves are eliminated, or the werewolves outnumber the villagers or util all the villagers complete all the tasks. It requires strategy, deduction, and persuasive skills to deceive or uncover the identities of the werewolves.

### Tech Stacks
![](https://img.shields.io/badge/OpenAI-412991.svg?stylee&logo=OpenAI&logoColor=white)
![](https://img.shields.io/badge/Python-3776AB.svg?stylee&logo=Python&logoColor=white)
![](https://img.shields.io/badge/PyGame-orange.svg?logo=Python&logoColor=white)
![](https://img.shields.io/badge/MongoDB-white.svg?logo=MongoDB&color=green)
![](https://img.shields.io/badge/PyTorch-db9f5e.svg?logo=PyTorch)
![](https://img.shields.io/badge/Docker-white?logo=Docker)
![](https://img.shields.io/badge/%F0%9F%A4%97-Transformers-yellow)


![Game Image](https://github.com/Mitulagr/GenerativeAgents/assets/32513766/74908d93-f860-432b-ba9d-d10b04f56963)



## Table Of Content

- [Installation](#installation)
- [Configuration](#configuration)
- [Game Instructions](#gameinstructions)
- [Contributors](#contributors)
- [Acknowledgements](#acknowledgements)


## Installation

Fork the repository using the button at the top or [this link](https://github.com/Mitulagr/GenerativeAgents/fork).

Clone the repository by typing in the Terminal
```
git clone https://github.com/< USERNAME >/GenerativeAgents.git
```

Navigate inside the directory
```
cd GenerativeAgents
```

Install all the libraries by entering the following commands

```
pip install -r requirements.txt
```

Go to Config folder and create a `.env` file.

Run the `Main.py` file


## Configuration

Setting up `.env` file

```
MongoDB_ID = < your MongoDB url for connection >
OpenAI_API_KEY = < your API_KEY from OPENAI >
OpenAI_Type = < your Type from OPENAI >
OpenAI_Base = < your OpenAI_Base >
OpenAI_Version = < your OpenAI_Version >
```

## Game Instruction

You can setup your own parameters to change the game balance as per your requirements. These are the following parameters which you can change or add more  :-

#### Inside `Params.py` file

* `agentsDetails` - has the name and description of agents

```
agentsDetails = [
    {"name": "Yumi Okada", "description": "Yumi is a werewolf; Yumi is smart, good at lying, and a farmer who works in the Cattle Farm. Also, Yumi tries to sabotage the tasks of the townfolks."},
    {"name": "Yuka Suzuki", "description": "Yuka is a townfolk; Yuka gets easily convinced by others' arguments and takes care of the well and its maintenance."},
    {"name": "Riku Mori", "description": "Riku is a townfolk; Riku is smart, has good deduction skills, and loves fishing in the Fishing area."},
    {"name": "Hina Sato", "description": "Hina is a townfolk; Hina is analytical and is a monk who works in the Shrine."},
    {"name": "Mana Yoshida", "description": "Mana is a werewolf; Mana is brilliant and an electrician who works in the Electricity House. Also, Mana tries to sabotage the tasks of the townfolks."},
    {"name": "Taichi Kato", "description": "Taichi is a townfolk and an electrician who does tasks at the Electricity House; Taichi is dumb."},
    {"name": "Yuria Shimizu", "description": "Yuria is a townfolk; Yuria has good convincing skills and is a farmer who works in the Cattle Farm."},
    {"name": "Haruka Itō", "description": "Haruka is a townfolk; Haruka has low convincing skills and is a fisherperson who works in the Fishing area. Haruka is friendly and loves talking"},
    # {"name": " ADD A NAME ", "description":" ADD A DESCRIPTION "}
]
```

* `TaskWin` - number of tasks needed to be completed for Townfolks to win

``` 
TasksWin = < Your number of tasks >
```

You can go through the code and change other parameters too, but you must be careful as you need to change multiple files and occurrences.

## Contributors

<br/>

<a href="">
  <img src="https://contrib.rocks/image?repo=Mitulagr/GenerativeAgents" />
</a>

<br/>

## Acknowledgement

We would like to thank all the mentors for there valuable suggestions. Without them this project could never be the way it is. We all have learned a lot of skills in the course of this project. Their dedication and expertise have been pivotal in shaping our project's success, and we are deeply grateful for their constant encouragement and support. The knowledge and skills we have acquired under their guidance will undoubtedly have a lasting impact on our personal and professional growth. Thank you for being instrumental in making this journey a truly enriching and transformative experience for all of us.

