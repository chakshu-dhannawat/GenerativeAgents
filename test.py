import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bonfire Animation")

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Define variables
fire_width = 300
fire_height = 400
fire_x = (width - fire_width) // 2
fire_y = height - fire_height

# Define fire particles
fire_particles = []

# Create fire particles
for _ in range(100):
    x = random.randint(fire_x, fire_x + fire_width)
    y = random.randint(fire_y, fire_y + fire_height)
    dx = random.uniform(-1, 1)
    dy = random.uniform(-2, -0.5)
    size = random.randint(1, 3)
    fire_particles.append((x, y, dx, dy, size))

# Fire animation variables

fire_animation_frames = [pygame.image.load(f'Assets\\Fire\\{i}.png') for i in range(40)]
fire_animation_frames.extend(fire_animation_frames[::-1])

current_frame = 0
frame_count = 0
animation_speed = 4  # Lower values make the animation faster

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update fire particles
    for i in range(len(fire_particles)):
        x, y, dx, dy, size = fire_particles[i]
        x += dx
        y += dy
        size -= 0.01
        if size <= 0:
            fire_particles[i] = (random.randint(fire_x, fire_x + fire_width),
                                 random.randint(fire_y, fire_y + fire_height),
                                 random.uniform(-1, 1),
                                 random.uniform(-2, -0.5),
                                 random.randint(1, 3))
        else:
            fire_particles[i] = (x, y, dx, dy, size)

    # Clear the screen
    window.fill(BLACK)

    # Draw central fire
    fire_image = pygame.transform.scale(fire_animation_frames[current_frame], (fire_width, fire_height))
    window.blit(fire_image, (fire_x, fire_y))

    # Update fire animation frames
    frame_count += 1
    if frame_count >= animation_speed:
        current_frame = (current_frame + 1) % len(fire_animation_frames)
        frame_count = 0

    # Draw fire particles
    for x, y, _, _, size in fire_particles:
        if size > 0:
            pygame.draw.circle(window, YELLOW, (int(x), int(y)), int(size))

    # Update the display
    pygame.display.flip()

    clock.tick(120)

# Quit the game
pygame.quit()
