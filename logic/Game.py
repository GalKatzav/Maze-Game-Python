import pygame
from logic.Player import Player
from logic.Menu import Menu
from interfaces.IGame import IGame
import random

class Game(IGame):
    def __init__(self):
        # אתחול Pygame
        pygame.init()

        # הגדרת צבעים
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)

        # הגדרת גודל חלון המשחק
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # הגדרת FPS
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # יצירת אובייקט של התפריט
        self.menu = Menu()
        self.player = None

        # טעינת סאונד
        self.sound_path = 'sounds/move.wav'
        self.move_sound = pygame.mixer.Sound(self.sound_path)
        self.win_sound_path = 'sounds/win.wav'
        self.win_sound = pygame.mixer.Sound(self.win_sound_path)

        # יצירת מבוך דינמי
        self.maze = None
        self.exit_position = None

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

        # בחירת מיקום סיום אקראי (חייב להיות תא ריק)
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
        else:  # hard
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
        player_rect = pygame.Rect(self.player.x - self.player.radius, self.player.y - self.player.radius, self.player.radius * 2, self.player.radius * 2)
        exit_rect = pygame.Rect(self.exit_position[0], self.exit_position[1], 20, 20)
        return player_rect.colliderect(exit_rect)

    def run(self):
        running = True
        in_menu = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if in_menu:
                    result = self.menu.handle_event(event)
                    if result:
                        color, difficulty = result
                        self.player = Player(30, 30, self.menu.get_selected_color(), self.move_sound)
                        self.set_difficulty(difficulty)
                        in_menu = False

            if in_menu:
                self.menu.draw(self.screen)
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player.move(-self.player.speed, 0, self.maze, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                if keys[pygame.K_RIGHT]:
                    self.player.move(self.player.speed, 0, self.maze, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                if keys[pygame.K_UP]:
                    self.player.move(0, -self.player.speed, self.maze, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                if keys[pygame.K_DOWN]:
                    self.player.move(0, self.player.speed, self.maze, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

                # ציור המסך והדמות
                self.screen.fill(self.WHITE)
                self.draw_maze()
                self.player.draw(self.screen)

                if self.check_win():
                    self.win_sound.play()
                    self.display_win_message()
                    pygame.time.wait(3000)  # המתנה של 3 שניות לפני היציאה
                    running = False

            # עדכון התצוגה
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()

    def display_win_message(self):
        font = pygame.font.Font(None, 74)
        text = font.render('You Win!', True, (0, 255, 0))
        self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, self.SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
