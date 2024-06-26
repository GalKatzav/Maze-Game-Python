from abc import ABC, abstractmethod

class IGame(ABC):
    @abstractmethod
    def run(self):
        pass
