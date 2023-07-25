import pyttsx3

# Dictionary to store the voice samples for each agent
# [各エージェントの音声サンプルを保存する辞書]
agent_voices = {
    'Agent1': 'path_to_voice_sample1',
    'Agent2': 'path_to_voice_sample2',
    'Agent3': 'path_to_voice_sample3',
    'Agent4': 'path_to_voice_sample4',
    'Agent5': 'path_to_voice_sample5'
}

def generate_voiceover(agent, text):
    engine = pyttsx3.init()

    # Set the voice sample for the agent [エージェントの音声サンプルを設定する]
    voice_sample = agent_voices.get(agent)
    if voice_sample is None:
        print("Voice sample not found for the agent.")
        return

    engine.setProperty('voice', voice_sample)

    # Convert the text to speech in Japanese [テキストを日本語で音声に変換します]
    engine.save_to_file(text, 'voiceover.wav')
    engine.runAndWait()