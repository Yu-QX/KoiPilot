from typing import Union
from ..config import ListenerConfig

def GetOllamaListener(config: Union[ListenerConfig, dict]) -> object:
    # If config is a dict, convert it to ListenerConfig
    if isinstance(config, dict):
        config = ListenerConfig(**config)
    
    # Get the Ollama listener
    if config.version == "v0.9.0":
        from .v0_9_0 import OllamaListener
        return OllamaListener(config)
    elif config.version == "v0.12":
        from .v0_12 import OllamaListener
        return OllamaListener(config)
    else:
        raise ValueError(f"Invalid Ollama version: {config.version}")