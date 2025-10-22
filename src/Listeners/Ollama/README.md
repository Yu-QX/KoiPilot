# Ollama Listener

This module provides an implementation of the Listener interface for interacting with Ollama AI servers.

## Versions

- **v0.9.0**: Original implementation using the `requests` library.
- **v0.12**: Updated implementation using Python's standard `urllib` library for improved compatibility and reduced dependencies.
  - Proper handling of non-JSON responses (like the root endpoint's "Ollama is running" message).
  - Improved error handling for HTTP errors and URL errors.
  - Fixed connection checking logic to work with Ollama's root endpoint.

## Usage

The specific version to use is determined by the main `Listeners` module based on configuration.