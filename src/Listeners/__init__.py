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
            from Ollama import GetOllamaListener
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
        result = self.listener.Generate(prompt, **kwargs)  # type: ignore
        return result if result is not None else ""

    def Chat(self, messages: list, **kwargs) -> str:
        """
        Generate a response to a given message.

        :param messages: The message list to generate a response to (history included).
        :param kwargs: Additional arguments for the AI API. Includes model, temperature, and other parameters.
        :return: The generated response.
        """
        result = self.listener.Chat(messages, **kwargs) # type: ignore
        return result if result is not None else ""
    
    def GenerateJson(self, prompt: str, **kwargs) -> dict:
        """
        Generate `json` based on a given prompt.

        :param prompt: The prompt to generate from.
        :param kwargs: Additional arguments for the AI API. Includes model, temperature, and other parameters.
        :return: The generated `JSON`.
        """
        result = self.listener.GenerateJson(prompt, **kwargs) # type: ignore
        return result if result is not None else {}

if __name__ == "__main__":
    listener = Listener()

    print("\n\n\n>>> GenerateJson:")
    prompt = "What can the weather be? Use json dictionary format with weather type as keys and explanations of each weather as values."
    result_json = listener.GenerateJson(prompt, seed=42)
    [print(f"{key}: {value}") for key, value in result_json.items()]

    print("\n\n\n>>> Chat:")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hello! 😊 How are you doing today? I'm here to help — feel free to ask me anything or just chat if that's what you're into too. What can I do for you?"},
        {"role": "user", "content": "Introduce yourself."},
    ]
    print(listener.Chat(messages=messages, seed=42))

    print("\n\n\n>>> Generate:")
    print(listener.Generate("Hello!", seed=42))
