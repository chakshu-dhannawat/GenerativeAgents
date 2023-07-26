# GenerativeAgents - ミラーズ・ホロウの狼たち

ミラーズ・ホロウの人狼」は、プレイヤーに町人、人狼、特別な登場人物という役割が割り当てられ、人狼を全滅させるか、人狼が村人の数を上回るか、与えられた課題をすべてクリアすることを目指す、人気のソーシャル推理ゲームだ。 

ゲーム中、プレイヤーは昼と夜のフェイズに参加する。ナイトフェイズでは、人狼が村人を選んで排除し、特定の特殊キャラクターが固有の能力を発揮することがある。日中、生き残ったプレイヤーは誰が人狼であるかについて議論し、投票する。最も多くの票を集めたプレイヤーが「リンチ」され、ゲームから除外される。

ゲームは昼と夜のフェイズを交互に繰り返し、人狼が全滅するか、人狼が村人を上回るまで、あるいは村人全員がすべての課題をクリアするまで続く。人狼の正体を欺いたり暴いたりするには、戦略、推理力、説得力が要求される。

### コードには理解を深めるために日本語のコメントがついている。

### Tech Stacks
![](https://img.shields.io/badge/OpenAI-412991.svg?stylee&logo=OpenAI&logoColor=white)
![](https://img.shields.io/badge/Python-3776AB.svg?stylee&logo=Python&logoColor=white)
![](https://img.shields.io/badge/PyGame-orange.svg?logo=Python&logoColor=white)
![](https://img.shields.io/badge/MongoDB-white.svg?logo=MongoDB&color=green)
![](https://img.shields.io/badge/PyTorch-db9f5e.svg?logo=PyTorch)
![](https://img.shields.io/badge/Docker-white?logo=Docker)
![](https://img.shields.io/badge/%F0%9F%A4%97-Transformers-yellow)


![Game Image](https://github.com/Mitulagr/GenerativeAgents/assets/32513766/74908d93-f860-432b-ba9d-d10b04f56963)



## 目次

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



<hr>