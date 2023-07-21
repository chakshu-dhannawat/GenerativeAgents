# Imports
from pygame.locals import *
from Params import *
import sys
import pygame

class Game_start():
    def __init__(self):

        pygame.font.init()
        pygame.init()
        self.window = None
        self.init_window()

    def init_window(self):
        pygame.font.init()
        pygame.init()

        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), RESIZABLE)
        pygame.display.set_caption("Werewolves of Miller Hollow")

    def get_window(self):

        return self.window

    def start(self):

        # Loading Asset
        start_phase = pygame.image.load('Assets/Phases/START~2.png')
        start_phase = pygame.transform.scale(start_phase, DEFAULT_IMAGE_SIZE)

        #Define Button for yes and no click
        yes_rect = pygame.Rect(742, 627, 150, 150)
        no_rect = pygame.Rect(1134, 623, 150, 150)


        yes_clicked = False
        while not yes_clicked:
            # Event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the user closes the window, exit the game
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the user clicked on a button
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_rect.collidepoint(mouse_pos):
                        # If the user clicked the yes button, break from the loop
                        yes_clicked = True
                    elif no_rect.collidepoint(mouse_pos):
                        # If the user clicked the no button, exit the game
                        pygame.quit()
                        sys.exit()

            # Blit the start_phase image on the window
            self.window.blit(start_phase, (0, 0))

            # Update the display
            pygame.display.update()
