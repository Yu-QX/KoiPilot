import os
import json, re

class MessageManager:
    """Handles all the messages."""
    def __init__(self):
        # User configurations
        self.LanguagePriorities = ["EN", "CN"]

        # System configurations
        self.accepted_file_suffixs = (".md", ".txt")
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
        message = ""
        if not message_id:
            return ""
        elif isinstance(message_id, (list, tuple)):
            # Sanitize each component to prevent path traversal
            message_id = [os.path.normpath(p).lstrip(os.path.pardir + os.sep) for p in message_id]
            message_path = os.path.join(self.messages_path, *message_id)
        else:
            message_id = os.path.normpath(message_id).lstrip(os.path.pardir + os.sep)
            message_path = os.path.join(self.messages_path, message_id)

        # if message_path is a folder, list the files in the folder and check for priority language
        if os.path.isdir(message_path):
            # Load and filter out not accepted file suffix
            all_files = os.listdir(message_path)
            files = [file for file in all_files if file.endswith(self.accepted_file_suffixs)]
            if not files:
                return ""

            for lang in self.LanguagePriorities:
                for suffix in self.accepted_file_suffixs:
                    if lang + suffix in files:
                        message_path = os.path.join(message_path, lang + suffix)
                        matched_lang = lang
                        break
            if not matched_lang:
                # choose the first file in the folder
                message_path = os.path.join(message_path, files[0])
                matched_lang = files[0].split(".")[0]
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

    def Construct(self, template_id: list[str] | tuple[str] | str, join_with: str = "\n\n", **kwargs) -> str | tuple[str, dict]:
        """
        Constructs a message by replacing placeholders with arguments.
        
        :param template_id: The template ID to retrieve. It is a list or tuple of strings indicating the indexes of the template to use.
        :param join_with: The string to join the blocks with.
        :param args: The arguments to replace placeholders in the message.
        :return: The constructed message, and the result format if any.
        """
        # Load template from template_id
        try:
            if not template_id:
                return ""
            elif isinstance(template_id, str):
                # Sanitize template_id to prevent path traversal
                if not template_id.endswith(".json"):
                    template_id += ".json"
                # Ensure safe path construction
                template_id = os.path.normpath(template_id).lstrip(os.path.pardir + os.sep)
                template_path = os.path.join(self.messages_path, template_id)
            else:
                # Convert tuple to list to allow modification
                template_id = list(template_id)
                if not template_id[-1].endswith(".json"):
                    template_id[-1] += ".json"
                # Sanitize each component to prevent path traversal
                template_id = [os.path.normpath(p).lstrip(os.path.pardir + os.sep) for p in template_id]
                template_path = os.path.join(self.messages_path, *template_id)
            with open(template_path, "r") as f:
                template = json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] Template file {template_id} not found.")
            return ""
        except json.JSONDecodeError:
            print(f"[ERROR] Template file {template_id} is not a valid JSON file.")
            return ""
        
        # Start parsing the template
        result = ""
        result_format = {}
        for block_id, block in template.items():
            # Ignore bad blocks
            if not isinstance(block, dict):
                continue

            # Check for special cases
            if block_id == "RESPONSE_FORMAT":
                result_format.update(block)

            # Use key: `message_id`, `message`
            raw_message = ""
            message_id = block.get("message_id")
            if isinstance(message_id, (list, tuple, str)):
                raw_message = self.GetMessage(message_id=message_id)
            if not raw_message:
                raw_message = block.get("message")
            if not isinstance(raw_message, str):
                continue
            
            # Check whether need formatting
            if block.get("dont_format", False):
                result += raw_message + join_with
                continue
            
            # Start formatting
            args_dict = kwargs
            # check args needed in the message
            args_needed = re.findall(r"\\{(\\d+)\\}", raw_message)
            # Check if all required arguments are present. If not, discard the block
            if not all(arg_id in args_dict for arg_id in args_needed):
                continue
            raw_message = raw_message.format(**args_dict)
            result += raw_message + join_with

        # Remove the last join_with, and return the result
        if result and join_with:
            result = result.rstrip(join_with).strip()

        if result_format:
            return result, result_format
        else:
            return result

    def SystemCode(self, code: int | str) -> str:
        """
        Returns the description of the given system code.
        
        :param code: The system code to retrieve the description for.
        :return: The description of the given system code.
        """
        try:
            return self.system_codes.get(str(code), "Unknown System Code")
        except Exception:
            return "Unknown System Code"
