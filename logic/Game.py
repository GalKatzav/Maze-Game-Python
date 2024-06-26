import pygame
from logic.Player import Player
from logic.Menu import Menu
from interfaces.IGame import IGame
import random


class Game(IGame):
    def __init__(self):  # Initialize Pygame
        pygame.init()

        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)

        # Define default screen size
        self.DEFAULT_SCREEN_WIDTH = 800
        self.DEFAULT_SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.DEFAULT_SCREEN_WIDTH, self.DEFAULT_SCREEN_HEIGHT))  # Create the game window
        self.SCREEN_WIDTH = self.DEFAULT_SCREEN_WIDTH
        self.SCREEN_HEIGHT = self.DEFAULT_SCREEN_HEIGHT

        # Define the clock and FPS (frames per second)
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.menu = Menu()  # Create a Menu object
        self.player = None  # Variable to store the player object

        # Load sound effects
        self.sound_path = 'sounds/move.wav'
        self.move_sound = pygame.mixer.Sound(self.sound_path)  # Load the move sound effect
        self.win_sound_path = 'sounds/win.wav'
        self.win_sound = pygame.mixer.Sound(self.win_sound_path)  # Load the win sound effect
        self.maze = None  # Variable to store the maze
        self.exit_position = None  # Variable to store the exit position

        # Load confetti images
        self.confetti_images = [
            pygame.image.load(f'pic/confetti/Confetti_{i:02d}.png') for i in range(1, 57)
        ]  # Load confetti images into a list
        self.confetti_frame = 0  # Variable to store the current confetti frame

    def generate_maze(self, width, height):
        """Generate a maze with the given width and height."""
        maze = [['#'] * width for _ in range(height)]  # Initialize the maze with walls ('#')

        def carve_passages_from(cx, cy):
            """Recursively carve passages in the maze starting from (cx, cy)."""
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Define possible directions (right, down, left, up)
            random.shuffle(directions)  # Shuffle the directions to randomize the maze
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy  # Calculate the next cell
                nx2, ny2 = cx + 2 * dx, cy + 2 * dy  # Calculate the cell two steps ahead
                if 0 <= nx2 < width and 0 <= ny2 < height and maze[ny2][nx2] == '#':  # Check if the next cell and the cell two steps ahead are within bounds and are walls
                    maze[ny][nx] = ' '  # Carve a passage
                    maze[ny2][nx2] = ' '  # Carve a passage two steps ahead
                    carve_passages_from(nx2, ny2)  # Recursively carve passages from the new cell

        maze[1][1] = ' '  # Start carving from (1, 1)
        carve_passages_from(1, 1)  # Start the recursive carving

        while True:  # Continuously search for a valid exit position in the maze
            exit_x = random.randint(0, width - 1)  # Randomly select an x-coordinate for the exit
            exit_y = random.randint(0, height - 1)  # Randomly select a y-coordinate for the exit
            if maze[exit_y][exit_x] == ' ': # Check if the randomly selected cell is an empty space
                maze[exit_y][exit_x] = 'E'  # Mark the exit in the maze
                break # Exit the loop once a valid exit position is found

        return maze, (exit_x * 20, exit_y * 20)  # Return the maze and the exit position

    def set_difficulty(self, difficulty):
        """Set the game difficulty by adjusting the screen size and maze dimensions."""
        if difficulty == 'easy':
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 400, 300
            maze_width, maze_height = 20, 15
        elif difficulty == 'medium':
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 600, 450
            maze_width, maze_height = 30, 22
        else:  # hard
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
            maze_width, maze_height = 40, 30

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))  # Set the screen size
        pygame.display.set_caption(f'Maze Game - {difficulty.capitalize()}')  # Set the window title
        self.maze, self.exit_position = self.generate_maze(maze_width, maze_height)  # Generate the maze

    def draw_maze(self):
        """Draw the maze on the screen."""
        for y, row in enumerate(self.maze):  # Iterate through each row and its index in the maze
            for x, char in enumerate(row):  # Iterate through each character and its index in the row
                if char == "#":
                    pygame.draw.rect(self.screen, self.BLACK, pygame.Rect(x * 20, y * 20, 20, 20))  # Draw a wall
                elif char == "E":
                    pygame.draw.rect(self.screen, self.GREEN, pygame.Rect(x * 20, y * 20, 20, 20))  # Draw the exit

    def check_win(self):
        """Check if the player has reached the exit."""
        player_rect = pygame.Rect(self.player.x - 10, self.player.y - 10, 20, 20)  # Create a rectangle around the player
        exit_rect = pygame.Rect(self.exit_position[0], self.exit_position[1], 20, 20)  # Create a rectangle around the exit
        return player_rect.colliderect(exit_rect)  # Check if the player collides with the exit

    def display_win_animation(self):
        """Display the win animation with confetti and play the win sound."""
        self.win_sound.play()  # Play the win sound
        for i in range(len(self.confetti_images)):   # Loop through all confetti images to create an animation
            self.screen.fill(self.WHITE)  # Fill the screen with white
            confetti_image = self.confetti_images[i]  # Get the current confetti image
            confetti_rect = confetti_image.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))  # Center the image
            self.screen.blit(confetti_image, confetti_rect)  # Draw the confetti image

            font = pygame.font.Font(None, 74)  # Load the font
            text = font.render('You Win!', True, (0, 255, 0))  # Render the win text
            self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, 50))  # Draw the win text at the top

            pygame.display.flip()  # Update the display
            pygame.time.wait(100)  # Wait 100 milliseconds between frames

    def run(self):
        """Run the game loop."""
        running = True  # Variable to control the main loop
        in_menu = True  # Variable to control if we are in the menu or in the game
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Check if the quit event is triggered
                    if in_menu:
                        running = False  # Exit the main loop if in the menu
                    else:
                        in_menu = True  # Go back to the menu if in the game
                        self.screen = pygame.display.set_mode((self.DEFAULT_SCREEN_WIDTH, self.DEFAULT_SCREEN_HEIGHT))  # Reset to default screen size

                if in_menu:
                    result = self.menu.handle_event(event)  # Handle menu events
                    if result:
                        difficulty = result  # Get the selected difficulty
                        self.player = Player(30, 30, self.move_sound)  # Create a player object
                        self.set_difficulty(difficulty)  # Set the game difficulty
                        in_menu = False  # Exit the menu

            if in_menu:
                self.menu.draw(self.screen)  # Draw the menu
            else:
                keys = pygame.key.get_pressed()  # Get the pressed keys
                dx, dy = 0, 0  # Initialize movement deltas
                if keys[pygame.K_LEFT]:
                    dx = -self.player.speed  # Move left
                if keys[pygame.K_RIGHT]:
                    dx = self.player.speed  # Move right
                if keys[pygame.K_UP]:
                    dy = -self.player.speed  # Move up
                if keys[pygame.K_DOWN]:
                    dy = self.player.speed  # Move down

                self.player.move(dx, dy, self.maze, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)   # Move the player

                self.screen.fill(self.WHITE)  # Fill the screen with white
                self.draw_maze()  # Draw the maze
                self.player.update()  # Update the player animation
                self.player.draw(self.screen)  # Draw the player

                if self.check_win():
                    self.display_win_animation()  # Display the win animation
                    pygame.time.wait(3000)  # Wait 3 seconds
                    in_menu = True
                    self.screen = pygame.display.set_mode((self.DEFAULT_SCREEN_WIDTH, self.DEFAULT_SCREEN_HEIGHT))  # Reset to default screen size

            pygame.display.flip()  # Update the display
            self.clock.tick(self.FPS)  # Cap the frame rate

        pygame.quit()  # Quit Pygame

    def display_win_message(self):
        """Display the win message."""
        font = pygame.font.Font(None, 74)  # Load the font
        text = font.render('You Win!', True, (0, 255, 0))  # Render the win text
        self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, 50))  # Draw the win text at the top
        pygame.display.flip()  # Update the display
