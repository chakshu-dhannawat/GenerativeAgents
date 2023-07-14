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
      Path = "Assets\\"
      x = self.rectangle.x
      y = self.rectangle.y
      bubble_image = pygame.image.load(Path+"hover_bubble.png")  # Replace "bubble.png" with the path to your predetermined image

      # Render the text
      font_size = 22  # Desired font size
      font = pygame.font.Font(None, font_size)
      font2 = pygame.font.SysFont('Comic Sans MS', font_size, pygame.font.Font.bold)
      font3 = pygame.font.SysFont('Comic Sans MS', font_size, pygame.font.Font.bold)
      
      # Split text into words
      words = self.desc.split()

      # Create lines of text with a maximum of 6 words per line
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

      # Calculate the maximum width and height for all lines
      max_width = 0
      total_height = 0
      for line in text_lines:
          text_surface = font.render(line, True, (0, 0, 0))
          max_width = max(max_width, text_surface.get_width())
          total_height += text_surface.get_height()

      # Create the bubble rectangle around the text
      bubble_padding = 20
      bubble_width = max_width + bubble_padding * 10 
      bubble_height = total_height + bubble_padding * 5 + 40
      
      # Blit the bubble image onto the surface
      scaled_bubble_image = pygame.transform.scale(bubble_image, (bubble_width, bubble_height))
      if(self.name == "Electricity House" or self.name =="Shrine" or self.name == "Hut 1"):
        bubble_rect = scaled_bubble_image.get_rect(bottomleft=(x, y))
      elif(self.name == "Fishing Pond"):
        bubble_rect = scaled_bubble_image.get_rect(topleft=(x, y))
      else:
          
        bubble_rect = scaled_bubble_image.get_rect(bottomright=(x, y))
      surface.blit(scaled_bubble_image, bubble_rect)
      task_print = False  
      # Blit the text onto the bubble
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
    def __init__(self, rectangle, font, text_color, box_color, name=None, desc=None, nextPlan=None):
        self.rectangle = rectangle
        # self.text = text
        self.name = name
        self.desc = desc
        self.plans = nextPlan
        self.font = font
        self.text_color = text_color
        self.box_color = box_color
        self.hovered = False

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
      Path = "Assets\\"
      x = self.rectangle.x
      y = self.rectangle.y
      bubble_image = pygame.image.load(Path+"agent_bubble.png")  # Replace "bubble.png" with the path to your predetermined image

      # Render the text
      font_size = 20  # Desired font size
      font = pygame.font.Font(None, font_size)
      font2 = pygame.font.SysFont('Comic Sans MS', font_size, pygame.font.Font.bold)
      font3 = pygame.font.SysFont('Comic Sans MS', font_size, pygame.font.Font.bold)
      

      # Split text into words
      words = self.desc.split()

      # Create lines of text with a maximum of 6 words per line
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

      # Create the bubble rectangle around the text
      bubble_padding = 20
      bubble_width = max_width + bubble_padding * 10
      bubble_height = total_height + bubble_padding * 8
      # bubble_rect = pygame.Rect(x - bubble_width // 2 - 50, y - bubble_height // 2 - 50, bubble_width, bubble_height)

      # Blit the bubble image onto the surface
      scaled_bubble_image = pygame.transform.scale(bubble_image, (bubble_width, bubble_height))
      
          
      bubble_rect = scaled_bubble_image.get_rect(bottomleft=(x-100, y+50))
      surface.blit(scaled_bubble_image, bubble_rect)

      # Blit the text onto the bubble
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