from datetime import datetime

class TerminalMessageInterface():
    def __init__(self):
        formatted_timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        file_name = "dominion" + formatted_timestamp + ".log"
        self.log_file = open(file_name, 'a')

    def send_message(self, message, player):
        self.log_file.write(message + '\n')
        print(message)

    def get_input(self, prompt, player):
        response = input(prompt)
        self.log_file.write(prompt + response + '\n')
        return response