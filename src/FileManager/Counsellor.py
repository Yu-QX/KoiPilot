import os, sys
from typing import Optional
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import difflib
from Listeners import Listener

# TODO: relocate this to `Messages`
def generate_prompt_move(file, folder_options, available_info: Optional[dict] = None) -> tuple[str, dict]:
    with open("src/FileManager/prompts/FileToFolder.md", "r") as f:
        prompt_FileToFolder = f.read()
    formatted_folders = "\n".join(f"- {folder}" for folder in folder_options)
    
    prompt = prompt_FileToFolder.format(file=file, folder_options=formatted_folders).strip()
    return prompt, {"result": "folder", "reason": "reason"}

# TODO: relocate this to `Messages`
def generate_prompt_name(name_list: list):
    with open("src/FileManager/prompts/FileName.md", "r") as f:
        prompt_Name = f.read()
    formatted_names = "\n".join(f"- {name}" for name in name_list)
    
    prompt = prompt_Name.format(name_list=formatted_names).strip()
    return prompt

def find_closest_match(string: str, options: list[str]) -> Optional[str]:
    """
    Finds the option most similar to the input string in a given list of options.
    
    This function first normalizes the options and input string to lowercase to ensure case-insensitive matching.
    Then, it uses the difflib library's get_close_matches method to find the closest match.
    If a sufficiently similar option is found (similarity score greater than 0.8), that option is returned;
    otherwise, it returns None.
    
    Parameters:
    string (str): The input string to match.
    options (list[str]): The list of options to match against.
    
    Returns:
    Optional[str]: The most similar option, or None if no sufficiently similar option is found.
    """
    
    # Normalize options and input string to lowercase for case-insensitive matching
    normalized_options = [name.lower() for name in options]
    normalized_input = string.lower()
    
    # Find the closest match, limiting to 1 result with a similarity score greater than 0.8
    closest_matches = difflib.get_close_matches(normalized_input, normalized_options, n=1, cutoff=0.8)
    
    # If a sufficiently similar option is found, return that option; otherwise, return None
    if closest_matches:
        result = options[normalized_options.index(closest_matches[0])]
    else:
        result = None
    
    return result



class Counsellor:
    """AI suggestions for file operations"""
    def __init__(self, model: Optional[str] = None, api_type: str = "ollama", host: str = "localhost", port: Optional[int] = None, api_key: Optional[str] = None, version: Optional[str] = None):
        self.listener = Listener(api_type, host, port, api_key, version)
        self.model = model

    def MoveToFolder(self, source: str, folder_options: list[str]) -> Optional[str]:
        """
        Suggests the best folder to move into based on AI analysis.
    
        :param source: The file or folder to move.
        :param folder_options: A list of potential folders to move the file into.
        :return: A string for the suggested folder.
        """
        # Gather available information & generate prompt
        available_info = {}                                                                     # TODO: add functions to `Operations` to enable this
        prompt, result_struct = generate_prompt_move(source, folder_options, available_info)    # TODO: Change name when `Messages` completed

        # Generate the suggestion
        suggestion = self.listener.GenerateJson(prompt=prompt, model=self.model, seed=42)

        # Parse the suggestion
        result_key = result_struct.get("result")
        if not isinstance(suggestion, dict) or result_key not in suggestion:
            return None
        
        result = suggestion[result_key]
        if result not in folder_options:
            result = find_closest_match(result, folder_options)
                
        return result
    
    def FormatName(self, name_list: list[str]) -> dict:
        """
        Suggest renamings for the given list of file or folder names to make them similar in format.
    
        :param name_list: A list of names to be formatted.
        :return: A dictionary containing the original names and their suggested new names.
        """
        # Generate prompt
        prompt = generate_prompt_name(name_list)
    
        # Generate response
        response = self.listener.GenerateJson(prompt, seed=42)
    
        # Parse response
        if not isinstance(response, dict):
            return {}
    
        changes = {}
        used_names = set()
    
        for original_name, suggested_name in response.items():
            if original_name not in name_list:
                original_name = find_closest_match(original_name, name_list)
            if original_name is None or original_name == suggested_name or suggested_name in used_names:
                continue
            changes[original_name] = suggested_name
            used_names.add(suggested_name)
    
        return changes