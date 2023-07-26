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

- [インストール](#インストール)
- [セットアップ](#セットアップ)
- [ゲームの説明](#ゲームの説明)
- [投稿者](#投稿者)
- [謝辞](#謝辞)


## インストール

一番上のボタンを使ってリポジトリをフォークするか [this link](https://github.com/Mitulagr/GenerativeAgents/fork).

ターミナルで次のように入力して、リポジトリをクローンします。
```
git clone https://github.com/< USERNAME >/GenerativeAgents.git
```

ディレクトリ内に移動する
```
cd GenerativeAgents
```

以下のコマンドを入力して、すべてのライブラリをインストールする。

```
pip install -r requirements.txt
```

Configフォルダに移動し、`.env` ファイルを作成する。

Main.py`ファイルを実行する。


## セットアップ

.env`ファイルの設定

```
MongoDB_ID = < your MongoDB url for connection >
OpenAI_API_KEY = < your API_KEY from OPENAI >
OpenAI_Type = < your Type from OPENAI >
OpenAI_Base = < your OpenAI_Base >
OpenAI_Version = < your OpenAI_Version >
```

## ゲームの説明

ゲームバランスを変更するために独自のパラメータを設定することができます。以下のパラメータを変更または追加することができます。

#### `Params.py` ファイルの中

* `agentsDetails` - エージェントの名前と説明がある

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

* `TaskWin` - タウンフォークスの優勝に必要なタスク数

``` 
TasksWin = < Your number of tasks >
```

しかし、複数のファイルやオカレンスを変更する必要があるため、注意が必要だ。

## 投稿者

<br/>

<a href="">
  <img src="https://contrib.rocks/image?repo=Mitulagr/GenerativeAgents" />
</a>

<br/>

## 謝辞

貴重なご指摘をいただいたすべてのメンターに感謝したい。彼らの存在なくして、このプロジェクトはあり得なかった。私たちは皆、このプロジェクトの過程で多くのスキルを学んだ。彼らの献身と専門知識は、私たちのプロジェクトを成功に導く上で極めて重要であり、彼らの絶え間ない励ましとサポートに深く感謝している。彼らの指導のもとで身につけた知識とスキルは、間違いなく私たちの個人的・職業的成長に永続的な影響を与えるだろう。この旅が、私たち全員にとって真に豊かで変容に満ちた経験となるよう尽力してくださったことに感謝します。



<hr>