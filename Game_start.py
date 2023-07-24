# This file contains the class Game_start which is responsible for the start phase of the game
# [このファイルにはGame_startクラスが含まれており、ゲームの開始フェーズを担当する。]

from pygame.locals import *
from Params import *
import sys
import pygame
import pyautogui

# Class for the start phase of the game [試合開始フェーズのクラス]
class Game_start():
    def __init__(self, window):

        pygame.font.init()
        pygame.init()
        self.window = window
        self.init_window()

    def init_window(self):
        # Set the window size [ウィンドウサイズの設定]
        pygame.display.set_caption("Werewolves of Miller Hollow")
        # Set the window icon [ウィンドウアイコンを設定する]
        # pyautogui.click(500, 500, button='left')
        # time.sleep(0.01)
        # pyautogui.moveTo(pyautogui.size()[0]-1,0)

    def get_window(self):
        return self.window

    # Start phase [スタート段階]
    def start(self):

        # Loading Asset [ローディング資産]
        start_phase = pygame.image.load('Assets/Phases/START~2.png')
        start_phase = pygame.transform.scale(start_phase, DEFAULT_IMAGE_SIZE)

        # Define Button for yes and no click [イエス・クリックとノー・クリックのボタンを定義する]
        yes_rect = pygame.Rect(742, 627, 150, 150)
        no_rect = pygame.Rect(1134, 623, 150, 150)

        # Loop for the start phase [スタートフェーズのループ]
        yes_clicked = False
        while not yes_clicked:
            # Event handling loop [イベント処理ループ]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_rect.collidepoint(mouse_pos):
                        # If the user clicked the yes button, break from the loop
                        # [ユーザーが「はい」ボタンをクリックした場合、ループから抜け出す]
                        yes_clicked = True
                    elif no_rect.collidepoint(mouse_pos):
                        # If the user clicked the no button, exit the game
                        # [ユーザーが「いいえ」ボタンをクリックした場合、ゲームを終了する。]
                        pygame.quit()
                        sys.exit()

            # Blit the start_phase image on the window [ウィンドウ上のstart_phase画像]
            self.window.blit(start_phase, (0, 0))

            # Update the display [ディスプレイの更新]
            pygame.display.update()
