from time import sleep

from eliot import to_file
from halo import Halo
from loguru import logger
import logging


class LoggingConfig:
    def __init__(self):
        self.spinner = self.initialize_spinner()
        self.configure_logger()
        self.configure_eliot()

    @staticmethod
    def configure_logger():
        # Configure Loguru
        logger.add("logs/app.log", rotation="10 MB")

        # Configure Python's built-in logger
        logging.basicConfig(filename='logs/python_logger.log', level=logging.INFO)

    @staticmethod
    def initialize_spinner():
        # Initialize Halo with a fun emoji
        spinner = Halo(text='🚀 Processing...', spinner='dots')
        return spinner  # return the spinner object

    @staticmethod
    def configure_eliot():
        # Direct Eliot's logs to a file
        to_file(open("logs/eliot.log", "w"))

    def start_spinner(self):
        # Start the spinner
        self.spinner.start()
        sleep(2)

    def stop_spinner(self):
        # Stop the spinner and add a fun emoji
        self.spinner.stop_and_persist(symbol='✅', text='Done!')


logging_config = LoggingConfig()
logging_config.configure_logger()
logging_config.initialize_spinner()
logging_config.configure_eliot()
logging_config.start_spinner()
logging_config.stop_spinner()

