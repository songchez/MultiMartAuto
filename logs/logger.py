import logging

class Logger:
    def __init__(self, log_file='logs/app.log'):
        """
        Initialize the Logger.
        :param log_file: Path to the log file.
        """
        self.log_file = log_file
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )

    def log_success(self, message):
        """
        Log a success message.
        :param message: Message to log.
        """
        logging.info(f"SUCCESS: {message}")

    def log_error(self, message):
        """
        Log an error message.
        :param message: Message to log.
        """
        logging.error(f"ERROR: {message}")
