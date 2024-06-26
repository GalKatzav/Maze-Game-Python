from abc import ABC, abstractmethod


# Define the IMenu interface using the Abstract Base Class (ABC) module
class IMenu(ABC):
    @abstractmethod
    def draw(self, screen):
        """Draw the menu on the screen."""
        pass

    @abstractmethod
    def handle_event(self, event):
        """Handle events such as keyboard input."""
        pass

    @abstractmethod
    def get_selected_difficulty(self):
        """Get the currently selected difficulty level."""
        pass
