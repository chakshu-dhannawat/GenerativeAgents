# This file contains the HoverTextBox class, which is used to create a box that appears when the mouse hovers over a particular location The box contains the name of the location and a description of the location. 
# [このファイルにはHoverTextBoxクラスが含まれています。このクラスは、マウスが特定の場所にカーソルを合わせたときに表示されるボックスを作成するために使用されます。]
# The box also contains the tasks that can be performed at that location.
# [ボックスには、その場所で実行できるタスクも表示される。]

import pygame
from Params import *

class HoverTextBox:
    def __init__(self, rectangle, font, text_color, box_color, name=None, desc=None, tasks=None):
        self.rectangle = rectangle
        # self.text = text
        self.name = name
        self.desc = desc
        self.tasks = tasks
        self.font = font
        self.text_color = text_color
        self.box_color = box_color
        self.hovered = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.box_color, self.rectangle)
        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surface, (self.rectangle.x + 10, self.rectangle.y + 10))
    
    # Function to handle the event when the mouse hovers over the location
    # [マウスがその位置にマウスオーバーしたときのイベントを処理する関数。]
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rectangle.collidepoint(event.pos):
                self.hovered = True
            else:
                self.hovered = False

    # Function to update the position of the box
    # [ボックスの位置を更新する関数]
    def update_position(self, x, y):
        self.rectangle.x = x
        self.rectangle.y = y

    # Function to display the box when the mouse hovers over the location
    # [マウスがその場所にカーソルを置いたときにボックスを表示する機能]    
    def hover_bubble(self,surface):
      Path = "Assets/"
      x = self.rectangle.x
      y = self.rectangle.y
      bubble_image = pygame.image.load(Path+"hover_bubble.png")  # Replace "bubble.png" with the path to your predetermined image ["bubble.png "を所定の画像へのパスに置き換える。]

      # Render the text [テキストのレンダリング]
      font_size = 22  # Desired font size [希望のフォントサイズ]
      font = pygame.font.Font(None, font_size)
      font2 = pygame.font.SysFont('Comic Sans MS', font_size, pygame.font.Font.bold)
      font3 = pygame.font.SysFont('Comic Sans MS', font_size, pygame.font.Font.bold)
      
      # Split text into words [テキストを単語に分割する]
      words = self.desc.split()

      # Create lines of text with a maximum of 6 words per line [1行最大6語のテキストを作成する。]
      text_lines = []
      line = ""
      text_lines.append(self.name)
      for word in words:
          if len(line.split()) < 8:
              line += " " + word
          else:
              text_lines.append(line.strip())
              line = word
      text_lines.append(line.strip())
      temp_task = self.tasks.split(':')
      if len(temp_task)>=2:
        tasks = temp_task[1].split('.')
        text_lines.append('Available Tasks:')
        for task in tasks[:-1]:
            task = "-> " + task
            line = ""
            for word in task.split():
                if len(line.split()) < 8:
                    line += " " + word
                else:
                    text_lines.append(line.strip())
                    line = word
            text_lines.append(line.strip())

      # Calculate the maximum width and height for all lines [すべての行の最大幅と高さを計算する]
      max_width = 0
      total_height = 0
      for line in text_lines:
          text_surface = font.render(line, True, (0, 0, 0))
          max_width = max(max_width, text_surface.get_width())
          total_height += text_surface.get_height()

      # Create the bubble rectangle around the text [テキストの周囲にバブル矩形を作成する]
      bubble_padding = 20
      bubble_width = max_width + bubble_padding * 10 
      bubble_height = total_height + bubble_padding * 5 + 40
      
      # Blit the bubble image onto the surface [表面に泡のイメージ]
      scaled_bubble_image = pygame.transform.scale(bubble_image, (bubble_width, bubble_height))
      if(self.name == "Electricity House" or self.name =="Shrine" or self.name == "Hut 1"):
        bubble_rect = scaled_bubble_image.get_rect(bottomleft=(x, y+50))
      elif(self.name == "Fishing Pond"):
        bubble_rect = scaled_bubble_image.get_rect(topleft=(x, y))
      else:
          
        bubble_rect = scaled_bubble_image.get_rect(bottomright=(x, y))
      surface.blit(scaled_bubble_image, bubble_rect)
      task_print = False  

      # Blit the text onto the bubble [テキストをバブルに]
      current_y = bubble_rect.top + bubble_padding*2.3
      for i,line in enumerate(text_lines):
        if(line == 'Available Tasks:'):
            text_surface = font2.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, top=current_y)
            surface.blit(text_surface, text_rect)
            current_y += text_surface.get_height()
            task_print = True
        elif(i==0):
            text_surface = font3.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, top=current_y)
            surface.blit(text_surface, text_rect)
            current_y += text_surface.get_height()           
        else:
            text_surface = font.render(line, True, (0, 0, 0))
            if task_print:
                text_rect = text_surface.get_rect(left=bubble_rect.left+100, top=current_y)
            else:
                text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, top=current_y)
            surface.blit(text_surface, text_rect)
            current_y += text_surface.get_height()



class HoverTextBox_Agent:
    def __init__(self, rectangle, font, text_color, box_color,agent, name=None, desc=None, nextPlan=None):
        self.rectangle = rectangle
        self.agent = agent
        self.name = name
        self.desc = desc
        self.plans = nextPlan
        self.font = font
        self.text_color = text_color
        self.box_color = box_color
        self.hovered = False
        self.WIN_WIDTH = 1920
        self.WIN_HEIGHT = 1080

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rectangle.collidepoint(event.pos):
                self.hovered = True
            else:
                self.hovered = False

    def update_position(self, x, y):
        self.rectangle.x = x
        self.rectangle.y = y
        
    def hover_bubble(self,surface):
      Path = "Assets/"
      x = self.rectangle.x
      y = self.rectangle.y
      bubble_image = pygame.image.load(Path+"agent_bubble.png")
      # Render the text [テキストのレンダリング]
      font_size = 20  # Desired font size [[希望のフォントサイズ]]
      font = pygame.font.Font(None, font_size)
      font2 = pygame.font.SysFont('Comic Sans MS', font_size, pygame.font.Font.bold)
      font3 = pygame.font.SysFont('Comic Sans MS', font_size, pygame.font.Font.bold)
      

      # Split text into words [テキストを単語に分割する]
      words = self.desc.split()
      text_lines = []
      line = ""
      text_lines.append(self.name)
      
      for word in words:
          if len(line.split()) < 8:
              line += " " + word
          else:
              text_lines.append(line.strip())
              line = word
      text_lines.append(line.strip())
      max_width = 0
      total_height = 0
      for line in text_lines:
          text_surface = font.render(line, True, (0, 0, 0))
          max_width = max(max_width, text_surface.get_width())
          total_height += text_surface.get_height()

      # Create the bubble rectangle around the text [テキストの周囲にバブル矩形を作成する]
      bubble_padding = 20
      bubble_width = max_width + bubble_padding * 10
      bubble_height = total_height + bubble_padding * 8
      
      # Blit the bubble image onto the surface [表面に泡のイメージ]
      scaled_bubble_image = pygame.transform.scale(bubble_image, (bubble_width, bubble_height))
      
      # setting the bubble position [バブル位置の設定]
      if(x > 1700) :
        bubble_rect = scaled_bubble_image.get_rect(bottomright=(x, y+50))
      else:
        bubble_rect = scaled_bubble_image.get_rect(bottomleft=(x-100, y+50))
      surface.blit(scaled_bubble_image, bubble_rect)

      # Blit the text onto the bubble [テキストをバブルに]
      current_y = bubble_rect.top + bubble_padding*3
      for i,line in enumerate(text_lines):
        if(line == 'My PLans:'):
            text_surface = font2.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, top=current_y)
            surface.blit(text_surface, text_rect)
            current_y += text_surface.get_height()
        elif(i==0):
            text_surface = font3.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, top=current_y)
            surface.blit(text_surface, text_rect)
            current_y += text_surface.get_height()           
        else:
            text_surface = font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, top=current_y)
            surface.blit(text_surface, text_rect)
            current_y += text_surface.get_height()

      transparency = 100
      radius = 35*3
      transparency_surface = pygame.Surface((self.WIN_WIDTH,self.WIN_HEIGHT), pygame.SRCALPHA)
      if self.agent.werewolf:
          radius = radius*1.5
          pygame.draw.circle(transparency_surface, (255, 0, 0, transparency), (x+self.agent.Character_Size[0]//2 +2, y+self.agent.Character_Size[0]//2+2), radius)
      else:
          pygame.draw.circle(transparency_surface, (0, 0, 255, transparency), (x+self.agent.Character_Size[0]//2 +2, y+self.agent.Character_Size[0]//2+2), radius)
      
      surface.blit(transparency_surface, (0,0))

    