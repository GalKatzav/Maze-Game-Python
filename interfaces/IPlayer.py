from abc import ABC, abstractmethod

class IPlayer(ABC):
    @abstractmethod
    def move(self, dx, dy, maze, screen_width, screen_height):
        pass

    @abstractmethod
    def draw(self, screen):
        pass
