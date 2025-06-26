import os
import datetime
import json, re, logging
from typing import Optional

# Path for datas and configs are in `snake_case`.
# Path for code and models are in `CamelCase`.
# Datas for models should be aligned with the model name if they are already contained in a `snake_case` folder.

START_TIME = datetime.datetime.now()
APP_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(APP_PATH, 'log')
CURRENT_LOG_FILE = os.path.join(LOG_PATH, f'{START_TIME.strftime("%Y-%m-%d_%H-%M-%S")}.log')
CONFIG_PATH = os.path.join(APP_PATH, 'config')
USER_SETTING_PATH = os.path.join(CONFIG_PATH, 'user_setting.json')
USAGE_RECORD_PATH = os.path.join(CONFIG_PATH, 'usage_record.json')

# Create paths if they don't exist
for path in [LOG_PATH, CONFIG_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)

# Load and save user settings

def LoadUserSettings() -> dict:
    if os.path.exists(USER_SETTING_PATH):
        with open(USER_SETTING_PATH, 'r') as f:
            return json.load(f)
    return {}

def SaveUserSettings(config: dict):
    with open(USER_SETTING_PATH, 'w') as f:
        json.dump(config, f, indent=2)

# Load and save usage record

def LoadUsageRecord() -> dict:
    if os.path.exists(USAGE_RECORD_PATH):
        with open(USAGE_RECORD_PATH, 'r') as f:
            return json.load(f)
    return {}

def SaveUsageRecord(record: dict):
    with open(USAGE_RECORD_PATH, 'w') as f:
        json.dump(record, f, indent=2)


# Configure logging
class Logger:
    """
    A class to handle logging operations.
    """

    def __init__(self, logger_name: str):
        """
        Initializes the Logger with the specified name.

        :param logger_name: The name of the logger.
        """
        self.logger_name = logger_name
        self.current_log_file = CURRENT_LOG_FILE

        logging.basicConfig(
            level=logging.INFO,
            filename=self.current_log_file,
            filemode='a',
            format='[%(asctime)s] %(name)s : %(message)s'
        )
        self.logger = logging.getLogger(logger_name)

    def Log(self, message: str):
        """
        Logs an informational message.

        :param message: The message to log.
        """
        self.logger.log(logging.INFO, message)

    def ReadLogs(self, log_file: Optional[str] = None) -> list:
        """
        Reads the contents of the application log file and parses it into a list of dictionaries.

        :param log_file: The path to the log file.
        :return: A list where each item is a dictionary containing 'timestamp', 'logger', and 'message'.
        """
        log_pattern = r'$([\d\-:\s,]+)$ (\w+) : (.*)'
        logs = []

        if log_file is None:
            log_file = CURRENT_LOG_FILE

        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                for line in f:
                    match = re.match(log_pattern, line.strip())
                    if match:
                        timestamp, logger, message = match.groups()
                        logs.append({
                            "timestamp": timestamp,
                            "logger": logger,
                            "message": message
                        })
        return logs

# Initial logging
logger = Logger("BASE")
logger.Log("Starting Running.")