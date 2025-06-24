import os
import json

class MessageManager:
    """Handles all the messages."""
    def __init__(self):
        # User configurations
        self.LanguagePriorities = ["EN", "CN"]

        # System configurations
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.messages_path = os.path.join(self.base_path, "MessageCenter")
        self.system_code_path = os.path.join(self.base_path, "SystemCodeCenter")

        self.system_codes = {}
        for file in os.listdir(self.system_code_path):
            if file.endswith(".json"):
                try:
                    with open(os.path.join(self.system_code_path, file), "r") as f:
                        self.system_codes.update(json.load(f))
                except json.JSONDecodeError:
                    print(f"Error loading {file}")
                    continue

    def GetMessage(self, message_id: list[str] | tuple[str] | str) -> str:
        """
        Returns the message corresponding to the given message ID.
        
        :param message_id: The message ID to retrieve. It is a list or tuple of strings indicating the indexes of the message.
        :return: The message corresponding to the given message ID.
        """
        matched_lang = None
        message = ""  # Initialize message to prevent unbound variable error
        if isinstance(message_id, (list, tuple)):
            message_path = os.path.join(self.messages_path, *message_id)
        else:
            message_path = os.path.join(self.messages_path, message_id)

        # if message_path is a folder, list the files in the folder and check for priority language
        if os.path.isdir(message_path):
            files = os.listdir(message_path)
            if not files:
                return ""
            for lang in self.LanguagePriorities:
                if lang + ".md" in files:
                    message_path = os.path.join(message_path, lang + ".md")
                    matched_lang = lang
                    break
                if lang + ".txt" in files:
                    message_path = os.path.join(message_path, lang + ".txt")
                    matched_lang = lang
                    break
            if not matched_lang:
                # choose the first file in the folder
                message_path = os.path.join(message_path, files[0])
                matched_lang = files[0].split(".")[-1]
            with open(message_path, "r", encoding="utf-8") as f:
                message = f.read()

        # if `message_path + ".json"` points to a JSON file, load it
        if os.path.exists(message_path + ".json"):
            try:
                with open(message_path + ".json", "r", encoding="utf-8") as f:
                    message_dict = json.load(f)
                if not message_dict:
                    return ""
            except json.JSONDecodeError:
                return ""
            
            for lang in self.LanguagePriorities:
                if lang in message_dict:
                    matched_lang = lang
                    message = message_dict[matched_lang]
                    break
            if matched_lang is None:
                matched_lang = message_dict.keys()[0]
                message = message_dict[matched_lang]

        if matched_lang is None:
            message = ""
        return message

    def Construct(self, message_id: list[str] | tuple[str] | str, *args) -> str:
        """
        Constructs a message by replacing placeholders with arguments.
        
        :param message_id: The message ID to retrieve. It is a list or tuple of strings indicating the indexes of the message.
        :param args: The arguments to replace placeholders in the message.
        :return: The constructed message.
        """
        return ""
    
    def SystemCode(self, code: int | str) -> str:
        """
        Returns the description of the given system code.
        
        :param code: The system code to retrieve the description for.
        :return: The description of the given system code.
        """
        message = "Unknown System Code"
        code = str(code)
        if code in self.system_codes:
            message = self.system_codes[code]
        return message