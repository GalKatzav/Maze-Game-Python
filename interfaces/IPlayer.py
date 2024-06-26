from abc import ABC, abstractmethod


# Define the IPlayer interface using the Abstract Base Class (ABC) module
class IPlayer(ABC):
    @abstractmethod
    def move(self, dx, dy, maze, screen_width, screen_height):
        """Move the player by (dx, dy) while checking collisions and bounds."""
        pass

    @abstractmethod
    def draw(self, screen):
        """Draw the player on the screen."""
        pass
