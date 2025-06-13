def GetOllamaListener(host, port, api_key, version) -> object:
    # Default values
    if host is None:
        host = "localhost"
    if port is None:
        port = 11434
    if version is None:
        version = "v0.9.0"

    # Get the Ollama listener
    if version == "v0.9.0":
        from .v0_9_0 import OllamaListener
        return OllamaListener(host, port, api_key)
    else:
        raise ValueError(f"Invalid Ollama version: {version}")
        # return 110102