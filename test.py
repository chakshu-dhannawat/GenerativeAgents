from Game import *

voice_sample = "Agent1_voice.mp3"

def speak(text):
    voicePath = voice_sample  # Assuming each voice sample is named as "{agent_name}_voice.mp3"
    translation = translator.translate(text)
    tts = gTTS(translation, lang='ja')
    tts.save(voicePath)
    # self.agents[curr].isSpeaking = True
    music = pygame.mixer.music.load(voicePath)
    pygame.mixer.music.play(1)
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.music.unload()
    # self.agents[curr].isSpeaking = False

text = "Hi, I am Hina Sato"
speak(text)