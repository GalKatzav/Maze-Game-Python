import pygame
from interfaces.IPlayer import IPlayer


class Player(IPlayer):
    def __init__(self, x, y, move_sound):
        """Initialize the player with position, speed, sounds, and images."""
        self.x = x  # X coordinate of the player
        self.y = y  # Y coordinate of the player
        self.speed = 5  # Speed of the player
        self.move_sound = move_sound  # Sound to play when the player moves

        # Load idle images
        self.idle_images = [
            pygame.image.load(f'pic/player/idle/adventurer-idle-2-00-1.3.png'),
            pygame.image.load(f'pic/player/idle/adventurer-idle-2-01-1.3.png'),
            pygame.image.load(f'pic/player/idle/adventurer-idle-2-02-1.3.png'),
            pygame.image.load(f'pic/player/idle/adventurer-idle-2-03-1.3.png')
        ]

        # Load run images
        self.run_images = [
            pygame.image.load(f'pic/player/run/adventurer-run3-00.png'),
            pygame.image.load(f'pic/player/run/adventurer-run3-01.png'),
            pygame.image.load(f'pic/player/run/adventurer-run3-02.png'),
            pygame.image.load(f'pic/player/run/adventurer-run3-03.png'),
            pygame.image.load(f'pic/player/run/adventurer-run3-04.png'),
            pygame.image.load(f'pic/player/run/adventurer-run3-05.png')
        ]

        self.current_image = self.idle_images[0]  # Set the initial image to the first idle image
        self.idle = True  # Player starts in idle state
        self.running = False  # Player is not running initially
        self.direction = 'right'  # Initial direction of the player
        self.last_update = pygame.time.get_ticks()  # Time of the last frame update
        self.frame_rate = 100  # Time between frames in milliseconds
        self.current_frame = 0  # Index of the current frame

    def move(self, dx, dy, maze, screen_width, screen_height):
        """Move the player by (dx, dy) if there are no collisions and within bounds."""
        if dx == 0 and dy == 0:
            self.idle = True  # Player is idle if not moving
            self.running = False  # Player is not running
        else:
            new_x = self.x + dx  # Calculate new x position
            new_y = self.y + dy  # Calculate new y position
            if not self.collides_with_walls(new_x, new_y, maze) and self.within_bounds(new_x, new_y, screen_width, screen_height):
                self.x = new_x  # Update x position
                self.y = new_y  # Update y position
                self.move_sound.play(maxtime=200)  # Play move sound, limited to 200ms
                self.idle = False  # Player is not idle
                self.running = True  # Player is running
                if dx > 0:
                    self.direction = 'right'  # Moving right
                elif dx < 0:
                    self.direction = 'left'  # Moving left
                elif dy > 0:
                    self.direction = 'down'  # Moving down
                elif dy < 0:
                    self.direction = 'up'  # Moving up
            else:
                self.idle = True  # Player is idle if collision or out of bounds
                self.running = False  # Player is not running

    def collides_with_walls(self, x, y, maze):
        """Check if the player collides with walls in the maze."""
        for row_index, row in enumerate(maze):  # Iterate through each row in the maze
            for col_index, char in enumerate(row):  # Iterate through each character in the row
                if char == "#":  # Check for wall character
                    wall_rect = pygame.Rect(col_index * 20, row_index * 20, 20, 20)  # Create wall rectangle
                    player_rect = pygame.Rect(x - 10, y - 10, 20, 20)  # Create player rectangle
                    if player_rect.colliderect(wall_rect):  # Check for collision
                        return True
        return False  # No collision

    def within_bounds(self, x, y, screen_width, screen_height):
        """Check if the player is within the screen bounds."""
        if x - 10 < 0 or x + 10 > screen_width:  # Check horizontal bounds
            return False
        if y - 10 < 0 or y + 10 > screen_height:  # Check vertical bounds
            return False
        return True  # Within bounds

    def update(self):
        """Update the player's animation frame."""
        now = pygame.time.get_ticks()  # Get current time
        if now - self.last_update > self.frame_rate:  # Check if it's time to update the frame
            self.last_update = now  # Update last update time
            self.current_frame = (self.current_frame + 1) % (len(self.run_images) if self.running else len(self.idle_images))  # Update current frame index
            if self.running:
                self.current_image = self.run_images[self.current_frame]  # Update to running image
            else:
                self.current_image = self.idle_images[self.current_frame]  # Update to idle image

    def draw(self, screen):
        """Draw the player on the screen with the correct orientation."""
        image = self.current_image  # Get the current image
        if self.direction == 'left':
            image = pygame.transform.flip(image, True, False)  # Flip image for left direction
        elif self.direction == 'up':
            image = pygame.transform.rotate(image, 90)  # Rotate image for up direction
        elif self.direction == 'down':
            image = pygame.transform.rotate(image, -90)  # Rotate image for down direction
        screen.blit(image, (self.x - image.get_width() // 2, self.y - image.get_height() // 2))  # Draw the image on the screen
