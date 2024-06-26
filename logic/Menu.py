import pygame
from interfaces.IMenu import IMenu


class Menu(IMenu):
    def __init__(self):
        """Initialize the menu, loading difficulty levels, GIF frames, and the move sound."""
        self.difficulties = ['easy', 'medium', 'hard']  # List of difficulty levels
        self.selected_difficulty = 0   # Index of the currently selected difficulty

        # Load GIF frames
        self.gif_frames = []  # List to store the GIF frames
        frame_count = 5  # Number of frames in the GIF
        for i in range(frame_count):
            frame_path = f'Pic/frame_{i}.png'  # Path to the current frame image
            frame = pygame.image.load(frame_path)  # Load the image from the file
            frame = pygame.transform.scale(frame, (800, 300))  # Scale the image to fit the screen
            self.gif_frames.append(frame)  # Add the image to the list of frames

        self.current_frame = 0  # Index of the current frame
        self.last_update = pygame.time.get_ticks()  # Time of the last frame update in milliseconds
        self.frame_rate = 300  # Time between frames in milliseconds

        # Load menu move sound
        self.move_sound_path = 'sounds/menu_move.wav'  # Path to the move sound file
        self.move_sound = pygame.mixer.Sound(self.move_sound_path)  # Load the move sound

    def draw(self, screen):
        """Draw the menu on the screen."""
        screen.fill((0, 0, 0))  # Fill the screen with black

        # Display GIF frames at the top of the page
        now = pygame.time.get_ticks()  # Get the current time
        if now - self.last_update > self.frame_rate:  # Check if it's time to update the frame
            self.last_update = now  # Update the last update time
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)  # Update the current frame index

        gif_image = self.gif_frames[self.current_frame]  # Get the current frame image
        screen.blit(gif_image, (0, 0))  # Draw the current frame image at the top of the screen

        font = pygame.font.Font(None, 36)  # Load the font
        for i, difficulty in enumerate(self.difficulties):  # Iterate through the difficulties
            color = (255, 255, 255) if i == self.selected_difficulty else (100, 100, 100)  # Set the color for the text
            text = font.render(difficulty, True, color)   # Render the difficulty text
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 320 + i * 40))  # Draw the text on the screen

    def handle_event(self, event):
        """Handle keyboard events to navigate the menu."""
        if event.type == pygame.KEYDOWN:  # Check if a key is pressed
            if event.key == pygame.K_UP:  # If the up arrow key is pressed
                self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)  # Move selection up
                self.move_sound.play()  # Play the move sound
            elif event.key == pygame.K_DOWN:  # If the down arrow key is pressed
                self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)  # Move selection down
                self.move_sound.play()  # Play the move sound
            elif event.key == pygame.K_RETURN:  # If the enter key is pressed
                return self.difficulties[self.selected_difficulty]  # Return the selected difficulty
        return None  # Return None if no selection is made

    def get_selected_difficulty(self):
        """Get the currently selected difficulty."""
        return self.difficulties[self.selected_difficulty]  # Return the selected difficulty
