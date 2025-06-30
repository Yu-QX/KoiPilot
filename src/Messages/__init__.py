import os
import json, re

# Helper function
def check_required_case(rc, args):
    """
    Checks whether the required case is satisfied based on the provided arguments.

    :param rc: The required case. It can be a string, a dictionary, or a list of strings or dictionaries.
               - If a string, checks if the corresponding argument exists in `args`.
               - If a dictionary, checks if all key-value pairs match those in `args`.
               - If a list, recursively checks each item in the list.
    :param args: A dictionary containing the arguments to check against the required case.
    :return: True if the required case is satisfied, False otherwise.
    """
    if isinstance(rc, str):
        return bool(args.get(rc))
    elif isinstance(rc, dict):
        return all(args.get(k) == v for k, v in rc.items())
    elif isinstance(rc, list):
        return all(check_required_case(item, args) for item in rc)
    else:
        return False

class MessageManager:
    """Handles all the messages."""
    def __init__(self):
        # User configurations
        self.LanguagePriorities = ["EN", "CN"]  # Language priority order

        # System configurations
        self.accepted_file_suffixs = (".md", ".txt")  # Accepted file extensions
        self.base_path = os.path.dirname(os.path.abspath(__file__))  # Base directory path
        self.messages_path = os.path.join(self.base_path, "message_center")  # Path to message files
        self.system_code_path = os.path.join(self.base_path, "system_code_center")  # Path to system code files

        self.system_codes = {}  # Dictionary to store system codes and their descriptions
        for file in os.listdir(self.system_code_path):
            if file.endswith(".json"):
                try:
                    with open(os.path.join(self.system_code_path, file), "r") as f:
                        self.system_codes.update(json.load(f))  # Load system codes from JSON files
                except json.JSONDecodeError:
                    print(f"Error loading {file}")  # Handle JSON decoding errors
                    continue

    def GetMessage(self, message_id: list[str] | tuple[str] | str) -> str:
        """
        Retrieves a message based on the given message ID.

        :param message_id: The message ID to retrieve. It can be a single string, a list, or a tuple indicating the indexes of the message.
        :return: The message corresponding to the given message ID, or an empty string if not found.
        """
        matched_lang = None
        message = ""
        if not message_id:
            return ""  # Return empty string if no message ID is provided
        elif isinstance(message_id, (list, tuple)):
            # Sanitize each component to prevent path traversal
            message_id = [os.path.normpath(p).lstrip(os.path.pardir + os.sep) for p in message_id]
            message_path = os.path.join(self.messages_path, *message_id)
        else:
            message_id = os.path.normpath(message_id).lstrip(os.path.pardir + os.sep)
            message_path = os.path.join(self.messages_path, message_id)

        # If message_path is a folder, list the files in the folder and check for priority language
        if os.path.isdir(message_path):
            # Load and filter out not accepted file suffix
            all_files = os.listdir(message_path)
            files = [file for file in all_files if file.endswith(self.accepted_file_suffixs)]
            if not files:
                return ""  # Return empty string if no valid files are found

            for lang in self.LanguagePriorities:
                for suffix in self.accepted_file_suffixs:
                    if lang + suffix in files:
                        message_path = os.path.join(message_path, lang + suffix)
                        matched_lang = lang
                        break
            if not matched_lang:
                # Choose the first file in the folder
                message_path = os.path.join(message_path, files[0])
                matched_lang = files[0].split(".")[0]
            with open(message_path, "r", encoding="utf-8") as f:
                message = f.read()  # Read the message content

        # If `message_path + ".json"` points to a JSON file, load it
        if os.path.exists(message_path + ".json"):
            try:
                with open(message_path + ".json", "r", encoding="utf-8") as f:
                    message_dict = json.load(f)  # Load JSON message content
                if not message_dict:
                    return ""  # Return empty string if JSON is empty
            except json.JSONDecodeError:
                return ""  # Return empty string if JSON decoding fails
            
            for lang in self.LanguagePriorities:
                if lang in message_dict:
                    matched_lang = lang
                    message = message_dict[matched_lang]
                    break
            if matched_lang is None:
                matched_lang = next(iter(message_dict.keys()))  # Use the first available language
                message = message_dict[matched_lang]

        if matched_lang is None:
            message = ""  # Set message to empty if no language matches
        return message

    def Construct(self, template_id: list[str] | tuple[str] | str, join_with: str = "\n\n", **kwargs) -> str | tuple[str, dict]:
        """
        Constructs a message by replacing placeholders with arguments based on a template.

        :param template_id: The template ID to retrieve. It can be a single string, a list, or a tuple indicating the indexes of the template.
        :param join_with: The string used to join multiple blocks of the constructed message. Default is "\n\n".
        :param kwargs: Keyword arguments representing placeholders to replace in the message.
        :return: A constructed message as a string, or a tuple containing the message and its result format if applicable.
        """
        args_dict = kwargs

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
            # Ignore bad blocks (non-dictionary types)
            if not isinstance(block, dict):
                continue
            
            # Check if the block has a required case and skip if not satisfied
            if block.get("case") and not check_required_case(block["case"], args_dict):
                continue

            # Handle special cases like RESPONSE_FORMAT
            if block_id == "RESPONSE_FORMAT":
                result_format.update(block)

            # Retrieve the raw message using either message_id or direct message content
            raw_message = ""
            message_id = block.get("message_id")
            if isinstance(message_id, (list, tuple, str)):
                raw_message = self.GetMessage(message_id=message_id)
            if not raw_message:
                raw_message = block.get("message")
            if not isinstance(raw_message, str):
                continue
            
            # Skip formatting if explicitly disabled
            if block.get("dont_format", False):
                result += raw_message + join_with
                continue
            
            # Format the message by replacing placeholders with provided arguments
            args_needed = re.findall(r"\\{(\\d+)\\}", raw_message)
            # Check if all required arguments are present; discard the block if not
            if not all(arg_id in args_dict for arg_id in args_needed):
                continue
            raw_message = raw_message.format(**args_dict)
            result += raw_message + join_with

        # Remove the last join_with delimiter and strip any extra whitespace
        if result and join_with:
            result = result.rstrip(join_with).strip()

        # Return the constructed message and result format if available
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
