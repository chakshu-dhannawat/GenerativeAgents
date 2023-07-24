# This file contains the class Game_start which is responsible for the start phase of the game

from pygame.locals import *
from Params import *
import sys
import pygame
# import pyautogui

# Class for the start phase of the game
class Game_start():
    def __init__(self, window):

        pygame.font.init()
        pygame.init()
        self.window = window
        self.init_window()

    def init_window(self):
        # Set the window size
        pygame.display.set_caption("Werewolves of Miller Hollow")
        # Set the window icon
        # pyautogui.click(500, 500, button='left')
        # time.sleep(0.01)
        # pyautogui.moveTo(pyautogui.size()[0]-1,0)

    def get_window(self):
        return self.window

    # Start phase
    def start(self):

        # Loading Asset
        start_phase = pygame.image.load('Assets/Phases/START~2.png')
        start_phase = pygame.transform.scale(start_phase, DEFAULT_IMAGE_SIZE)

        #Define Button for yes and no click
        yes_rect = pygame.Rect(742, 627, 150, 150)
        no_rect = pygame.Rect(1134, 623, 150, 150)

        # Loop for the start phase
        yes_clicked = False
        while not yes_clicked:
            # Event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
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
