from typing import Optional

class Listener:
    """
    The `Listeners` module manages all interactions with AI APIs.
    """
    def __init__(self, api_type: str = "ollama", host: str = "localhost", port: Optional[int] = None, api_key: Optional[str] = None, version: Optional[str] = None):
        """
        Initialize the `Listener` class.

        Args:
            api_type (str, optional): The type of AI API to use. Defaults to "ollama".
            host (str, optional): The host of the AI API. Defaults to "localhost".
            port (int, optional): The port of the AI API. Defaults to None.
            api_key (str, optional): The API key for authentication. Defaults to None.
            version (str, optional): The version of the AI API. Defaults to None.
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

        Returns:
            object: The loaded AI API object.
        """
        if self.api_type == "ollama":
            from Ollama import GetOllamaListener
            return GetOllamaListener(self.host, self.port, self.api_key, self.version)
        else:
            raise ValueError(f"Invalid API type: {self.api_type}")
            # return 110001
    
    def Generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text based on a given prompt.

        Args:
            prompt (str): The prompt to generate text from.
            **kwargs: Additional arguments for the AI API. Includes model, temperature, and other parameters.

        Returns:
            str: The generated text.
        """
        return self.listener.Generate(prompt, **kwargs) # type: ignore

    def Chat(self, messages: list, **kwargs) -> str:
        """
        Generate a response to a given message.

        Args:
            messages (str): The message list to generate a response to (history included).
            **kwargs: Additional arguments for the AI API. Includes model, temperature, and other parameters.

        Returns:
            str: The generated response.
        """
        return self.listener.Chat(messages, **kwargs) # type: ignore

if __name__ == "__main__":
    listener = Listener()
    
    print(listener.Generate("Hello!", seed=42))

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hello! 😊 How are you doing today? I'm here to help — feel free to ask me anything or just chat if that's what you're into too. What can I do for you?"},
        {"role": "user", "content": "Introduce yourself."},
    ]
    print(listener.Chat(messages=messages, seed=42))