import os
import datetime
import json
import logging
import re
from typing import Optional

# Path for datas and configs are in `snake_case`.
# Path for code and models are in `CamelCase`.
# Datas for models should be aligned with the model name if they are already contained in a `snake_case` folder.

START_TIME = datetime.datetime.now()
APP_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(APP_PATH, 'log')
CURRENT_LOG_FILE = os.path.join(LOG_PATH, f'{START_TIME.strftime("%Y-%m-%d_%H-%M-%S")}.log')
CONFIG_PATH = os.path.join(APP_PATH, 'config')
USER_SETTING_FILE = os.path.join(CONFIG_PATH, 'user_setting.json')
USAGE_RECORD_FILE = os.path.join(CONFIG_PATH, 'usage_record.json')
PATH_SECURITY_FILE = os.path.join(CONFIG_PATH, 'path_security.json')

# Create paths if they don't exist
for path in [LOG_PATH, CONFIG_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)

# Use default settings if no settings file exists

DEFAULT_USER_SETTING = {}

DEFAULT_USAGE_RECORD = {}


def load_json_with_backup(file_path, default_data, entity_name):
    """
    Helper function to load JSON data from a file with error handling and backup.

    :param file_path: Path to the JSON file.
    :param default_data: Default data to restore if file is missing or corrupted.
    :param entity_name: Name of the entity being loaded, for logging purposes.
    :return: Loaded JSON data or default_data if error occurred.
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default_data, f, indent=2)
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        backup_path = f"{file_path}.corrupted_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        os.rename(file_path, backup_path)
        Logger("BASE").Log(f"Corrupted {entity_name} backed up to {backup_path}")
        with open(file_path, 'w') as f:
            json.dump(default_data, f, indent=2)
        return default_data


class UserSetting:
    """A class to handle user settings."""
    def __init__(self):
        self.path = USER_SETTING_FILE
        self.settings = self.Load()

    def Load(self) -> dict:
        """
        Loads user settings from the file.

        :return: The loaded user settings.
        """
        return load_json_with_backup(self.path, DEFAULT_USER_SETTING, "user settings")

    def Save(self):
        """
        Saves the user settings to the file.
        """
        with open(self.path, 'w') as f:
            json.dump(self.settings, f, indent=2)

    def Update(self, **kwargs):
        """
        Updates user settings with the provided keyword arguments.

        :param kwargs: Keyword arguments to update the settings.
        """
        self.settings.update(kwargs)
        self.Save()

    def Get(self, key):
        """
        Gets a setting value by key.

        :param key: The key of the setting to retrieve.
        :return: The value of the setting, or None if the key does not exist.
        """
        return self.settings.get(key)

class UsageRecord:
    """A class to handle usage records."""
    def __init__(self):
        self.path = USAGE_RECORD_FILE
        self.record = self.Load()

    def Load(self) -> dict:
        """
        Loads usage record from the file.

        :return: The loaded usage record.
        """
        return load_json_with_backup(self.path, DEFAULT_USAGE_RECORD, "usage record")

    def Save(self):
        """
        Saves the usage record to the file.
        """
        with open(self.path, 'w') as f:
            json.dump(self.record, f, indent=2)

    def Update(self, **kwargs):
        """
        Updates usage record with the provided keyword arguments.

        :param kwargs: Keyword arguments to update the record.
        """
        self.record.update(kwargs)
        self.Save()

    def Get(self, key):
        """
        Gets a usage record value by key.

        :param key: The key of the record to retrieve.
        :return: The value of the record, or None if the key does not exist.
        """
        return self.record.get(key)

class Logger:
    """A class to handle logging operations."""
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