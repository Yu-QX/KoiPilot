import json
import requests
from typing import Optional
from urllib.parse import urljoin

class OllamaListener:
    def __init__(self, host: str = "localhost", port: int = 11434, api_key: Optional[str] = None):
        self.host = host
        self.port = port
        self.api_key = api_key
        
        self.url = f"http://{self.host}:{self.port}"
        self.headers = {
            "Content-Type": "application/json"
        }

        if not self.check_connection():
            print("Failed to connect to Ollama server")
            self.connection_error = True
        else:
            self.connection_error = False
        
        if self.api_key:
            print("API key is currently not supported.")

    def check_connection(self) -> bool:
        try:
            response = requests.get(self.url)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def pick_model(self) -> Optional[str]:
        full_url = urljoin(self.url, "/api/tags")
        try:
            response = requests.get(full_url, timeout=5)
            response.raise_for_status()
            models = response.json().get("models", [])
            if not isinstance(models, list) or len(models) == 0 or "name" not in models[0]:
                print("Invalid or empty model data received.")
                return None
            return models[0]["name"]
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error fetching models: {e}")
            return None

    def GenerateRaw(self, prompt: str, **kwargs) -> Optional[dict]:
        """The basic generation function"""
        # Check connection
        self.check_connection()
        if self.connection_error:
            print("Cannot generate due to connection error.")
            return None

        # Prepare data
        data = {
            "prompt": prompt,
            "stream": False,
        }
        for key, value in kwargs.items():
            if value is not None:
                data[key] = value

        if "model" not in data:
            data["model"] = self.pick_model()
            if data["model"] is None:
                print("No valid model found.")
                return None

        # Generate
        endpoint = "/api/generate"
        full_url = urljoin(self.url, endpoint)

        try:
            response = requests.post(
                full_url,
                headers=self.headers,
                json=data,
                stream=False,
            )
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error generating: {e}")
            return None
    
    def ChatRaw(self, messages: list, **kwargs) -> Optional[dict]:
        """The basic chat function"""
        # Check connection
        self.check_connection()
        if self.connection_error:
            print("Cannot chat due to connection error.")
            return None
        
        # Prepare data
        data = {
            "messages": messages,
            "stream": False,
        }
        for key, value in kwargs.items():
            if value is not None:
                data[key] = value

        if "model" not in data:
            data["model"] = self.pick_model()
            if data["model"] is None:
                print("No valid model found.")
                return None
        
        # Chat
        endpoint = "/api/chat"
        full_url = urljoin(self.url, endpoint)
        try:
            response = requests.post(
                full_url,
                headers=self.headers,
                json=data,
                stream=False,
            )
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error generating: {e}")
            return None
        
    def Generate(self, prompt: str, **kwargs) -> Optional[str]:
        """Generate returning with string"""
        result = self.GenerateRaw(prompt, **kwargs)
        if result is None:
            print("Generation failed!")
            return None
        if not isinstance(result, dict):
            print("Unexpected content format in 'response'")
            return None
        
        return result.get("response")

    def Chat(self, messages: list, **kwargs) -> Optional[str]:
        """Chat returning with string"""
        result = self.ChatRaw(messages, **kwargs)
        if result is None:
            print("Chatting failed!")
            return None
    
        message = result.get("message")
        if not isinstance(message, dict):
            print("Unexpected content format in 'message'")
            return None

        return message.get("content")

    def GenerateJson(self, prompt: str, **kwargs) -> Optional[dict]:
        """Generate returning with JSON"""
        kwargs["format"] = "json"
        result = self.GenerateRaw(prompt, **kwargs)
        if result is None:
            print("Generation failed!")
            return None
        if not isinstance(result, dict):
            print("Unexpected content format in 'response'")
        
        response = result.get("response")
        if not isinstance(response, str):
            print("Response content is not a string, cannot parse as JSON.")
            return None
        
        # Parse JSON
        try:
            # Find valid JSON boundaries
            start_idx = response.find("{")
            end_idx = response.rfind("}")
            if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
                print("No valid JSON structure found.")
                return None

            json_str = response[start_idx:end_idx + 1]
            result_json = json.loads(json_str)
        except json.JSONDecodeError:
            print("Failed to parse JSON")
            result_json = None

        return result_json