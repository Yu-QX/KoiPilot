import os, sys
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional

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
        self.model = self.pick_model()

        if self.api_key:
            self.logger.Log("<110001> API key is currently not supported.")

    def _make_request(self, method: str, url: str, data: Optional[bytes] = None, timeout: int = 5) -> Optional[dict]:
        """
        Helper function to make HTTP requests using urllib.

        :param method: HTTP method (GET, POST)
        :param url: Full URL to make the request to
        :param data: Data to send in the request body (for POST)
        :param timeout: Request timeout in seconds
        :return: JSON response as a dictionary or None if an error occurred
        """
        try:
            req = urllib.request.Request(url, data=data, headers=self.headers, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                response_data = response.read().decode('utf-8')
                # Check if response is JSON
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    return json.loads(response_data)
                else:
                    # For non-JSON responses, log the content and return None
                    self.logger.Log(f"<110121> Non-JSON response received from {url}: {response_data}")
                    return None
        except urllib.error.HTTPError as e:
            # Read the response body for HTTP errors
            error_body = e.read().decode('utf-8') if e.fp else "No error body"
            self.logger.Log(f"<110121> HTTP Error {e.code}: {e.reason} for URL {url}. Response body: {error_body}")
            return None
        except urllib.error.URLError as e:
            self.logger.Log(f"<110122> URL Error: {e.reason} for URL {url}")
            return None
        except json.JSONDecodeError as e:
            self.logger.Log(f"<110121> JSON Decode Error: {e} for URL {url}")
            return None
        except Exception as e:
            self.logger.Log(f"<110121> Unexpected error during request: {e} for URL {url}")
            return None

    def check_connection(self) -> bool:
        try:
            req = urllib.request.Request(self.url)
            with urllib.request.urlopen(req, timeout=5) as response:
                # Check if we got a response, regardless of content type
                if response.status == 200:
                    self.connection_error = False
                    self.logger.Log("<110100> Connected to Ollama server")
                    return True
                else:
                    self.connection_error = True
                    self.logger.Log(f"<110122> Failed to connect to Ollama server at {self.url} with status {response.status}")
                    return False
        except Exception as e:
            self.logger.Log(f"<110122> Failed to connect to Ollama server at {self.url}: {e}")
            self.connection_error = True
            return False

    def pick_model(self) -> Optional[str]:
        model_list = self.GetModels()
        if model_list:
            self.logger.Log("<110100> Model list retrieved successfully.")
            return model_list[0]["name"]
        else:
            self.logger.Log("<110112> No valid model found.")
            return None

    def GetModels(self) -> Optional[list[dict]]:
        """Get all available models"""
        full_url = urllib.parse.urljoin(self.url, "/api/tags")
        result = self._make_request("GET", full_url, timeout=5)
        if result is None:
            return None

        models = result.get("models", [])
        if not isinstance(models, list) or len(models) == 0 or "name" not in models[0]:
            self.logger.Log("<110112> Invalid or empty model data received.")
            return None
        return models

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
            data["model"] = self.model
            if data["model"] is None:
                self.logger.Log("<110112> No valid model found.")
                return None

        # Generate
        endpoint = "/api/generate"
        full_url = urllib.parse.urljoin(self.url, endpoint)
        data_bytes = json.dumps(data).encode('utf-8')

        return self._make_request("POST", full_url, data=data_bytes, timeout=30)

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
            data["model"] = self.model
            if data["model"] is None:
                self.logger.Log("<110112> No valid model found.")
                return None

        # Chat
        endpoint = "/api/chat"
        full_url = urllib.parse.urljoin(self.url, endpoint)
        data_bytes = json.dumps(data).encode('utf-8')

        return self._make_request("POST", full_url, data=data_bytes, timeout=30)

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

    def SetModel(self, model: Optional[str] = None):
        """Set the model to use for generation"""
        if (not isinstance(model, str)) or (not model):
            self.logger.Log("<110112> Invalid model name provided.")
            return
        # Check whether model exists
        models = self.GetModels()
        if models is None or not any(m['name'] == model for m in models):
            self.logger.Log("<110112> Model not found.")
            return
        self.model = model
        self.logger.Log(f"<110100> Model set to {model}")