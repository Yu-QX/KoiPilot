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

    def GenerateDetail(self, prompt: str, **kwargs) -> Optional[dict]:
        # Check connection
        self.check_connection()
        if self.connection_error:
            print("Cannot generate detail due to connection error.")
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
            print(f"Error generating detail: {e}")
            return None
    
    def Generate(self, prompt: str, **kwargs) -> Optional[str]:
        result = self.GenerateDetail(prompt, **kwargs)
        if result is None:
            print("Generation failed!")
            return None
        return result.get("response")
