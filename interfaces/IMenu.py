from abc import ABC, abstractmethod

class IMenu(ABC):
    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def get_selected_color(self):
        pass

    @abstractmethod
    def get_selected_difficulty(self):
        pass
