from abc import ABC, abstractmethod

class MessageInterface(ABC):
    @abstractmethod
    def send_message(self, message, player):
        """Send a message to a specific player."""
        pass

    @abstractmethod
    def get_input(self, message, player):
        """Get input from a specific player."""
        pass

    @abstractmethod
    def broadcast_message(self, message):
        """Broadcast a message to all players."""
        pass