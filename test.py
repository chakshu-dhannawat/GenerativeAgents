from Game import *

pygame.font.init()
pygame.init()
DEFAULT_IMAGE_SIZE = (WIN_WIDTH, WIN_HEIGHT)

speed = FPS*0.6


'''
====================
Assests
====================
'''

font = pygame.font.SysFont('comicsans', 30, True)
font2 = pygame.font.SysFont('consolas', 25, True)

bg = pygame.image.load(Path+'town.png')
bg2 = pygame.image.load(Path+'blackbg.png')

bgs = [pygame.image.load(Path+f'Background\\{i}.png') for i in range(100)]

music = pygame.mixer.music.load(Path+'music.mp3')
pygame.mixer.music.play(-1)
