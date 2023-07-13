import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Progress Bar Example")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define progress bar dimensions
progress_bar_width = window_width - 40
progress_bar_height = 30
progress_bar_x = 20
progress_bar_y = 20

# Define the maximum value for the progress bar
TasksMax = 100

# Set the initial value for the progress bar
TasksDone = 10

font = pygame.font.Font(None, 24)

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the window
    window.fill(WHITE)

    # Calculate the width of the progress bar based on the current progress
    progress_width = (TasksDone / TasksMax) * progress_bar_width

    pygame.draw.rect(window, BLACK, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)

    center_x = progress_bar_x + progress_bar_width / 2
    center_y = progress_bar_y + progress_bar_height / 2

    text_surface = font.render(f"Tasks Progress", True, BLACK)

    # Get the rectangle of the text surface
    text_rect = text_surface.get_rect()

    # Calculate the position to center the text on the progress bar
    text_rect.center = (math.ceil(center_x), math.ceil(center_y))

    # Draw the text on the window
    window.blit(text_surface, text_rect)

    pygame.draw.rect(window, (34, 139, 24), (progress_bar_x+2, progress_bar_y+2, progress_width-4, progress_bar_height-4))

    pygame.display.flip()

pygame.quit()
