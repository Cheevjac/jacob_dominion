from GameLog import GameLog
from MessageInterface import MessageInterface

class TerminalMessageInterface(MessageInterface):
    def __init__(self, config):
        self.game_log = GameLog(logging_directory=config["logging_directory"])

    def send_message(self, message, player):
        self.game_log.log(f"{message}")
        print(message)

    def get_input(self, prompt, player):
        response = input(prompt)
        self.game_log.log(f"Prompt:{prompt} Response:{response}")
        return response

    def broadcast_message(self, message):
        self.game_log.log(f"Broadcast:{message}")
        print(f"{message}")
