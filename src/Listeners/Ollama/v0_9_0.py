import os, sys
import json
import requests
from typing import Optional
from urllib.parse import urljoin

APP_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

from Environment import Logger

class OllamaListener:
    def __init__(self, host: str = "localhost", port: int = 11434, api_key: Optional[str] = None):
        self.logger = Logger("OllamaListener")
        self.host = host
        self.port = port
        self.api_key = api_key
        
        self.url = f"http://{self.host}:{self.port}"
        self.headers = {
            "Content-Type": "application/json"
        }

        self.check_connection()

        if self.api_key:
            self.logger.Log("<110001> API key is currently not supported.")

    def check_connection(self) -> bool:
        try:
            response = requests.get(self.url)
            self.connection_error = response.status_code != 200
            if self.connection_error:
                self.logger.Log(f"<110122> Failed to connect to Ollama server at {self.url}")
                return False
            else:
                self.logger.Log("<110100> Connected to Ollama server")
                return True
        except requests.exceptions.RequestException:
            self.logger.Log(f"<110122> Failed to connect to Ollama server at {self.url}")
            self.connection_error = True
            return False

    def pick_model(self) -> Optional[str]:
        full_url = urljoin(self.url, "/api/tags")
        try:
            response = requests.get(full_url, timeout=5)
            response.raise_for_status()
            models = response.json().get("models", [])
            if not isinstance(models, list) or len(models) == 0 or "name" not in models[0]:
                self.logger.Log("<110112> Invalid or empty model data received.")
                return None
            return models[0]["name"]
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            self.logger.Log(f"<110121> Error fetching models: {e}")
            return None

    def GenerateRaw(self, prompt: str, **kwargs) -> Optional[dict]:
        """The basic generation function"""
        # Check connection
        self.check_connection()
        if self.connection_error:
            self.logger.Log("<110122> Cannot generate due to connection error.")
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
                self.logger.Log("<110112> No valid model found.")
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
            self.logger.Log(f"<110121> Error generating: {e}")
            return None
    
    def ChatRaw(self, messages: list, **kwargs) -> Optional[dict]:
        """The basic chat function"""
        # Check connection
        self.check_connection()
        if self.connection_error:
            self.logger.Log("<110122> Cannot chat due to connection error.")
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
                self.logger.Log("<110112> No valid model found.")
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
            self.logger.Log(f"<110121> Error chatting: {e}")
            return None
        
    def Generate(self, prompt: str, **kwargs) -> Optional[str]:
        """Generate returning with string"""
        result = self.GenerateRaw(prompt, **kwargs)
        if result is None:
            self.logger.Log("<110111> Generation failed!")
            return None
        if not isinstance(result, dict):
            self.logger.Log("<110111> Unexpected content format in 'response'")
            return None
        
        return result.get("response")

    def Chat(self, messages: list, **kwargs) -> Optional[str]:
        """Chat returning with string"""
        result = self.ChatRaw(messages, **kwargs)
        if result is None:
            self.logger.Log("<110111> Chatting failed!")
            return None
    
        message = result.get("message")
        if not isinstance(message, dict):
            self.logger.Log("<110111> Unexpected content format in 'message'")
            return None

        return message.get("content")

    def GenerateJson(self, prompt: str, **kwargs) -> Optional[dict]:
        """Generate returning with JSON"""
        kwargs["format"] = "json"
        result = self.GenerateRaw(prompt, **kwargs)
        if result is None:
            self.logger.Log("<110111> Generation failed!")
            return None
        if not isinstance(result, dict):
            self.logger.Log("<110111> Unexpected content format in 'response'")
        
        response = result.get("response")
        if not isinstance(response, str):
            self.logger.Log("<110111> Response content is not a string, cannot parse as JSON.")
            return None
        
        # Parse JSON
        try:
            # Find valid JSON boundaries
            start_idx = response.find("{")
            end_idx = response.rfind("}")
            if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
                self.logger.Log("<110111> No valid JSON structure found.")
                return None

            json_str = response[start_idx:end_idx + 1]
            result_json = json.loads(json_str)
        except json.JSONDecodeError:
            self.logger.Log("<110111> Failed to parse JSON")
            result_json = None

        return result_json