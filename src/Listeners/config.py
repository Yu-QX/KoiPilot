import os
import sys
from dataclasses import dataclass
from typing import Optional

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

from Environment import Logger

@dataclass
class ListenerConfig:
    """Configuration class for Listener"""
    api_type: str = "ollama"
    host: str = "localhost"
    port: Optional[int] = None
    api_key: Optional[str] = None
    version: Optional[str] = None
    
    def __post_init__(self):
        # Set default port based on API type if not provided
        if self.port is None:
            if self.api_type == "ollama":
                self.port = 11434
            # Add other API types here if needed
        
        # Set default version based on API type if not provided
        if self.version is None:
            if self.api_type == "ollama":
                self.version = "v0.12"
            # Add other API types here if needed
        
        # Validate version for Ollama
        if self.api_type == "ollama":
            if self.version not in ["v0.9.0", "v0.12"]:
                logger = Logger("ListenerConfig")
                logger.Log(f"Invalid Ollama version: {self.version}. Using default v0.12.")
                self.version = "v0.12"