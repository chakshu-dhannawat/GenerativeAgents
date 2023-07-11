import pygame

class HoverTextBox:
    def __init__(self, rectangle, text, font, text_color, box_color):
        self.rectangle = rectangle
        self.text = text
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
      text = self.text
      x = self.rectangle.x
      y = self.rectangle.y
      bubble_image = pygame.image.load(Path+"speechbubble_png_blue.png")  # Replace "bubble.png" with the path to your predetermined image

      # Render the text
      font_size = 22  # Desired font size
      font = pygame.font.Font(None, font_size)

      # Split text into words
      words = text.split()

      # Create lines of text with a maximum of 6 words per line
      text_lines = []
      line = ""
      
      text_lines.append(words[0])
      words = words[1:]
      
      for word in words:
          if len(line.split()) < 6:
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
      bubble_height = total_height + bubble_padding * 4
      # bubble_rect = pygame.Rect(x - bubble_width // 2 - 50, y - bubble_height // 2 - 50, bubble_width, bubble_height)

      # Blit the bubble image onto the surface
      scaled_bubble_image = pygame.transform.scale(bubble_image, (bubble_width, bubble_height))
      bubble_rect = scaled_bubble_image.get_rect(bottomright=(x+bubble_width//4, y))
      surface.blit(scaled_bubble_image, bubble_rect)

      # Blit the text onto the bubble
      current_y = bubble_rect.top + bubble_padding
      for line in text_lines:
          text_surface = font.render(line, True, (0, 0, 0))
          text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, top=current_y)
          surface.blit(text_surface, text_rect)
          current_y += text_surface.get_height()