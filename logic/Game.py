import pygame
from logic.Player import Player
from logic.Menu import Menu
from interfaces.IGame import IGame
import random


class Game(IGame):
    def __init__(self):
        pygame.init()

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)

        self.DEFAULT_SCREEN_WIDTH = 800
        self.DEFAULT_SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.DEFAULT_SCREEN_WIDTH, self.DEFAULT_SCREEN_HEIGHT))
        self.SCREEN_WIDTH = self.DEFAULT_SCREEN_WIDTH
        self.SCREEN_HEIGHT = self.DEFAULT_SCREEN_HEIGHT

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.menu = Menu()
        self.player = None

        self.sound_path = 'sounds/move.wav'
        self.move_sound = pygame.mixer.Sound(self.sound_path)
        self.win_sound_path = 'sounds/win.wav'
        self.win_sound = pygame.mixer.Sound(self.win_sound_path)

        self.maze = None
        self.exit_position = None

        # Load confetti images
        self.confetti_images = [
            pygame.image.load(f'pic/confetti/Confetti_{i:02d}.png') for i in range(1, 57)
        ]
        self.confetti_frame = 0

    def generate_maze(self, width, height):
        maze = [['#'] * width for _ in range(height)]

        def carve_passages_from(cx, cy):
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                nx2, ny2 = cx + 2 * dx, cy + 2 * dy
                if 0 <= nx2 < width and 0 <= ny2 < height and maze[ny2][nx2] == '#':
                    maze[ny][nx] = ' '
                    maze[ny2][nx2] = ' '
                    carve_passages_from(nx2, ny2)

        maze[1][1] = ' '
        carve_passages_from(1, 1)

        while True:
            exit_x = random.randint(0, width - 1)
            exit_y = random.randint(0, height - 1)
            if maze[exit_y][exit_x] == ' ':
                maze[exit_y][exit_x] = 'E'
                break

        return maze, (exit_x * 20, exit_y * 20)

    def set_difficulty(self, difficulty):
        if difficulty == 'easy':
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 400, 300
            maze_width, maze_height = 20, 15
        elif difficulty == 'medium':
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 600, 450
            maze_width, maze_height = 30, 22
        else:
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
            maze_width, maze_height = 40, 30

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(f'Maze Game - {difficulty.capitalize()}')
        self.maze, self.exit_position = self.generate_maze(maze_width, maze_height)

    def draw_maze(self):
        for y, row in enumerate(self.maze):
            for x, char in enumerate(row):
                if char == "#":
                    pygame.draw.rect(self.screen, self.BLACK, pygame.Rect(x * 20, y * 20, 20, 20))
                elif char == "E":
                    pygame.draw.rect(self.screen, self.GREEN, pygame.Rect(x * 20, y * 20, 20, 20))

    def check_win(self):
        player_rect = pygame.Rect(self.player.x - 10, self.player.y - 10, 20, 20)
        exit_rect = pygame.Rect(self.exit_position[0], self.exit_position[1], 20, 20)
        return player_rect.colliderect(exit_rect)

    def display_win_animation(self):
        for i in range(len(self.confetti_images)):
            self.screen.fill(self.WHITE)
            confetti_image = self.confetti_images[i]
            confetti_rect = confetti_image.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
            self.screen.blit(confetti_image, confetti_rect)

            font = pygame.font.Font(None, 74)
            text = font.render('You Win!', True, (0, 255, 0))
            self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

            pygame.display.flip()
            pygame.time.wait(100)  # Wait 100 milliseconds between frames

    def run(self):
        running = True
        in_menu = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if in_menu:
                        running = False
                    else:
                        in_menu = True
                        self.screen = pygame.display.set_mode((self.DEFAULT_SCREEN_WIDTH, self.DEFAULT_SCREEN_HEIGHT))

                if in_menu:
                    result = self.menu.handle_event(event)
                    if result:
                        difficulty = result
                        self.player = Player(30, 30, self.move_sound)
                        self.set_difficulty(difficulty)
                        in_menu = False

            if in_menu:
                self.menu.draw(self.screen)
            else:
                keys = pygame.key.get_pressed()
                dx, dy = 0, 0
                if keys[pygame.K_LEFT]:
                    dx = -self.player.speed
                if keys[pygame.K_RIGHT]:
                    dx = self.player.speed
                if keys[pygame.K_UP]:
                    dy = -self.player.speed
                if keys[pygame.K_DOWN]:
                    dy = self.player.speed

                self.player.move(dx, dy, self.maze, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

                self.screen.fill(self.WHITE)
                self.draw_maze()
                self.player.update()
                self.player.draw(self.screen)

                if self.check_win():
                    self.win_sound.play()
                    self.display_win_animation()
                    pygame.time.wait(3000)
                    in_menu = True
                    self.screen = pygame.display.set_mode((self.DEFAULT_SCREEN_WIDTH, self.DEFAULT_SCREEN_HEIGHT))

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()

    def display_win_message(self):
        font = pygame.font.Font(None, 74)
        text = font.render('You Win!', True, (0, 255, 0))
        self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, 50))
        pygame.display.flip()
