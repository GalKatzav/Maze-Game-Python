import pygame
from interfaces.IPlayer import IPlayer

class Player(IPlayer):
    def __init__(self, x, y, move_sound):
        self.x = x
        self.y = y
        self.speed = 5
        self.move_sound = move_sound

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

        self.current_image = self.idle_images[0]
        self.idle = True
        self.running = False
        self.direction = 'right'
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Time between frames in milliseconds
        self.current_frame = 0

    def move(self, dx, dy, maze, screen_width, screen_height):
        if dx == 0 and dy == 0:
            self.idle = True
            self.running = False
        else:
            new_x = self.x + dx
            new_y = self.y + dy
            if not self.collides_with_walls(new_x, new_y, maze) and self.within_bounds(new_x, new_y, screen_width, screen_height):
                self.x = new_x
                self.y = new_y
                self.move_sound.play(maxtime=200)
                self.idle = False
                self.running = True
                if dx > 0:
                    self.direction = 'right'
                elif dx < 0:
                    self.direction = 'left'
                elif dy > 0:
                    self.direction = 'down'
                elif dy < 0:
                    self.direction = 'up'
            else:
                self.idle = True
                self.running = False

    def collides_with_walls(self, x, y, maze):
        for row_index, row in enumerate(maze):
            for col_index, char in enumerate(row):
                if char == "#":
                    wall_rect = pygame.Rect(col_index * 20, row_index * 20, 20, 20)
                    player_rect = pygame.Rect(x - 10, y - 10, 20, 20)
                    if player_rect.colliderect(wall_rect):
                        return True
        return False

    def within_bounds(self, x, y, screen_width, screen_height):
        if x - 10 < 0 or x + 10 > screen_width:
            return False
        if y - 10 < 0 or y + 10 > screen_height:
            return False
        return True

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % (len(self.run_images) if self.running else len(self.idle_images))
            if self.running:
                self.current_image = self.run_images[self.current_frame]
            else:
                self.current_image = self.idle_images[self.current_frame]

    def draw(self, screen):
        image = self.current_image
        if self.direction == 'left':
            image = pygame.transform.flip(image, True, False)
        elif self.direction == 'up':
            image = pygame.transform.rotate(image, 90)
        elif self.direction == 'down':
            image = pygame.transform.rotate(image, -90)
        screen.blit(image, (self.x - image.get_width() // 2, self.y - image.get_height() // 2))
