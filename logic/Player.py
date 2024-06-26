import pygame
from interfaces.IPlayer import IPlayer


class Player(IPlayer):
    def __init__(self, x, y, color, move_sound):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = color
        self.speed = 5
        self.move_sound = move_sound

    def move(self, dx, dy, maze, screen_width, screen_height):
        new_x = self.x + dx
        new_y = self.y + dy
        if not self.collides_with_walls(new_x, new_y, maze) and self.within_bounds(new_x, new_y, screen_width, screen_height):
            self.x = new_x
            self.y = new_y
            self.move_sound.play(maxtime=200)

    def collides_with_walls(self, x, y, maze):
        for row_index, row in enumerate(maze):
            for col_index, char in enumerate(row):
                if char == "#":
                    wall_rect = pygame.Rect(col_index * 20, row_index * 20, 20, 20)
                    player_rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
                    if player_rect.colliderect(wall_rect):
                        return True
        return False

    def within_bounds(self, x, y, screen_width, screen_height):
        if x - self.radius < 0 or x + self.radius > screen_width:
            return False
        if y - self.radius < 0 or y + self.radius > screen_height:
            return False
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
