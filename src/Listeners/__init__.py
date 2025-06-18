from typing import Optional

class Listener:
    """
    The `Listener` class manages all interactions with AI APIs.
    It provides methods for generating text, handling chat interactions, and generating JSON responses.
    """

    def __init__(self, api_type: str = "ollama", host: str = "localhost", port: Optional[int] = None, api_key: Optional[str] = None, version: Optional[str] = None):
        """
        Initialize the `Listener` class.

        :param api_type: The type of AI API to use. Defaults to "ollama".
        :param host: The host of the AI API. Defaults to "localhost".
        :param port: The port of the AI API. Defaults to None.
        :param api_key: The API key for authentication. Defaults to None.
        :param version: The version of the AI API. Defaults to None.
        """
        self.api_type = api_type
        self.api_key = api_key
        self.host = host
        self.port = port
        self.version = version
        self.listener = self.load_listener()
    
    def load_listener(self) -> object:
        """
        Load the appropriate AI API based on the `api_type`.

        :return: The loaded AI API object.
        """
        if self.api_type == "ollama":
            from .Ollama import GetOllamaListener
            return GetOllamaListener(self.host, self.port, self.api_key, self.version)
        else:
            raise ValueError(f"Invalid API type: {self.api_type}")

    def Generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text based on a given prompt.

        :param prompt: The prompt to generate text from.
        :param kwargs: Additional arguments for the AI API. Includes model, temperature, and other parameters.
        :return: The generated text.
        """
        # Check if the function is available
        if not hasattr(self.listener, "Generate"):
            return ""
        result = self.listener.Generate(prompt, **kwargs)  # type: ignore
        return result if result is not None else ""

    def Chat(self, messages: list, **kwargs) -> str:
        """
        Generate a response to a given message.

        :param messages: The message list to generate a response to (history included).
        :param kwargs: Additional arguments for the AI API. Includes model, temperature, and other parameters.
        :return: The generated response.
        """
        if not hasattr(self.listener, "Chat"):
            return ""
        result = self.listener.Chat(messages, **kwargs) # type: ignore
        return result if result is not None else ""
    
    def GenerateJson(self, prompt: str, **kwargs) -> dict:
        """
        Generate `json` based on a given prompt.

        :param prompt: The prompt to generate from.
        :param kwargs: Additional arguments for the AI API. Includes model, temperature, and other parameters.
        :return: The generated `JSON`.
        """
        if not hasattr(self.listener, "GenerateJson"):
            return {}
        result = self.listener.GenerateJson(prompt, **kwargs) # type: ignore
        return result if result is not None else {}
