from datetime import datetime

class GameLog:
    def __init__(self, logging_directory):
        # Create a timestamped log file
        formatted_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{logging_directory}/dominion_{formatted_timestamp}.log"
        self.log_file = open(file_name, 'a')
    
    def log(self, message):
        # Write a timestamped message to the log file
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_file.write(f"[{timestamp}]:{message}\n")
    
    def close(self):
        # Close the log file when done
        self.log_file.close()