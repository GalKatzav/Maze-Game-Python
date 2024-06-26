from abc import ABC, abstractmethod


# Define the IGame interface using the Abstract Base Class (ABC) module
class IGame(ABC):
    @abstractmethod
    def run(self):
        """Run the main game loop."""
        pass
