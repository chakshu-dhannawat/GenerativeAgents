import pygame
import emoji

def generateEmoji(emoji_alias):
    # Initialize Pygame
    pygame.init()

    # Define the window dimensions
    window_width = 400
    window_height = 400

    # Create the window
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Emoji Display")

    # Load the emoji font
    font_size = 100
    emoji_font = pygame.font.Font(None, font_size)

    # Define the emoji to display
    emoji_text = emoji.emojize(emoji_alias)

    # Render the emoji as text
    emoji_text_rendered = emoji_font.render(emoji_text, True, (255, 255, 255))

    # Get the dimensions of the rendered text
    text_width, text_height = emoji_text_rendered.get_size()

    # Calculate the position to center the text in the window
    text_x = (window_width - text_width) // 2
    text_y = (window_height - text_height) // 2

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the window
        window.fill((0, 0, 0))

        # Draw the emoji text in the center of the window
        window.blit(emoji_text_rendered, (text_x, text_y))

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()

# Generate and display a specific emoji
generateEmoji(":smile:")