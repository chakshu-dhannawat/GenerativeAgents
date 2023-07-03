from gtts import gTTS
from Params import *
import pygame
from pygame.locals import *
from Game import *

pygame.font.init()
pygame.init()

def generate_voiceover_japanese(text):
    tts = gTTS(text, lang='ja')
    tts.save("voiceover_japanese.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("voiceover_japanese.mp3")
    pygame.mixer.music.play(-1)

# Example usage
text = "Hello, I am the virtual agent."
generate_voiceover_japanese(text)
