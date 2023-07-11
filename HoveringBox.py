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