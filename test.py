import pygame
import math

pygame.init()

# Set up the display
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Load the character image
character_image = pygame.image.load("Assets\\character_01\\D1.png")
character_rect = character_image.get_rect()

# Set the initial position and rotation of the character
character_x = -character_rect.width
character_y = screen_height // 2 - character_rect.height // 2
rotation_angle = 0

# Set the animation variables
speed = 5
rotation_speed = 5

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update character position and rotation
    character_x += speed
    rotation_angle += rotation_speed
    if character_x > screen_width:
        character_x = -character_rect.width

    # Clear the screen
    screen.fill((255, 255, 255))

    # Rotate the character image
    rotated_image = pygame.transform.rotate(character_image, rotation_angle)

    # Draw the rotated character image
    screen.blit(rotated_image, (character_x, character_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
