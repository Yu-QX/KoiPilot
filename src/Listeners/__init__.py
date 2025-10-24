import os, sys
from typing import Optional, Union
from dataclasses import asdict

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

from Environment import Logger
from .config import ListenerConfig

class Listener:
    """
    The `Listener` class manages all interactions with AI APIs.
    It provides methods for generating text, handling chat interactions, and generating JSON responses.
    """

    def __init__(self, 
                 config: Optional[ListenerConfig] = None, 
                 api_type: Optional[str] = None, 
                 host: Optional[str] = None, 
                 port: Optional[int] = None, 
                 api_key: Optional[str] = None, 
                 version: Optional[str] = None):
        """
        Initialize the `Listener` class.

        :param config: A ListenerConfig object with all configuration parameters.
        :param api_type: The type of AI API to use. Defaults to "ollama".
        :param host: The host of the AI API. Defaults to "localhost".
        :param port: The port of the AI API. Defaults to None.
        :param api_key: The API key for authentication. Defaults to None.
        :param version: The version of the AI API. Defaults to None.
        """
        self.logger = Logger("Listener")
        
        # If no config provided, create one with the provided parameters or defaults
        if config is None:
            # Use provided parameters or None (will be set to defaults in ListenerConfig)
            config_params = {
                k: v for k, v in {
                    'api_type': api_type,
                    'host': host,
                    'port': port,
                    'api_key': api_key,
                    'version': version
                }.items() if v is not None
            }
            config = ListenerConfig(**config_params)
        # If both config and parameters provided, merge them (parameters take precedence)
        elif any(param is not None for param in [api_type, host, port, api_key, version]):
            config_dict = asdict(config)
            config_dict.update({
                k: v for k, v in {
                    'api_type': api_type,
                    'host': host,
                    'port': port,
                    'api_key': api_key,
                    'version': version
                }.items() if v is not None
            })
            config = ListenerConfig(**config_dict)
            
        self.config = config
        self.listener = self.load_listener()
    
    def load_listener(self) -> object:
        """
        Load the appropriate AI API based on the `api_type`.

        :return: The loaded AI API object.
        """
        if self.config.api_type == "ollama":
            from .Ollama import GetOllamaListener
            return GetOllamaListener(self.config)
        else:
            self.logger.Log(f"<110001> Invalid API type:")
            raise ValueError(f"Invalid API type:")

    def Generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text based on a given prompt.

        :param prompt: The prompt to generate text from.
        :param kwargs: Additional arguments for the AI API. Includes model, temperature, and other parameters.
        :return: The generated text.
        """
        # Check if the function is available
        if not hasattr(self.listener, "Generate"):
            self.logger.Log(f"<110021> The API does not support text generation.")
            return ""
        result = self.listener.Generate(prompt, **kwargs)  # type: ignore
        if not result:
            self.logger.Log(f"<110011> The API returned an empty response when Generate.")
        else:
            self.logger.Log(f"<110000> Generate succeeded.")
        return result if result is not None else ""

    def Chat(self, messages: list, **kwargs) -> str:
        """
        Generate a response to a given message.

        :param messages: The message list to generate a response to (history included).
        :param kwargs: Additional arguments for the AI API. Includes model, temperature, and other parameters.
        :return: The generated response.
        """
        if not hasattr(self.listener, "Chat"):
            self.logger.Log(f"<110021> The API does not support chatting.")
            return ""
        result = self.listener.Chat(messages, **kwargs) # type: ignore
        if not result:
            self.logger.Log(f"<110011> The API returned an empty response when Chat.")
        else:
            self.logger.Log(f"<110000> Generate succeeded.")
        return result if result is not None else ""
    
    def GenerateJson(self, prompt: str, **kwargs) -> dict:
        """
        Generate `json` based on a given prompt.

        :param prompt: The prompt to generate from.
        :param kwargs: Additional arguments for the AI API. Includes model, temperature, and other parameters.
        :return: The generated `JSON`.
        """
        if not hasattr(self.listener, "GenerateJson"):
            self.logger.Log(f"<110021> The API does not support JSON generation.")
            return {}
        result = self.listener.GenerateJson(prompt, **kwargs) # type: ignore
        if not result:
            self.logger.Log(f"<110011> Failed to generate JSON.")
        else:
            self.logger.Log(f"<110000> Generate succeeded.")
        return result if result is not None else {}

    def SetModel(self, model: Optional[str] = None):
        """
        Set the model for the AI API.

        :param model: The model to set.
        """
        if not isinstance(model, str):
            self.logger.Log(f"<110011> Invalid model: {model}")
        if hasattr(self.listener, "SetModel"):
            self.listener.SetModel(model) # type: ignore
        else:
            self.logger.Log(f"<110021> The API does not support default model.")