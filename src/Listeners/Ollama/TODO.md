# TODO

# Done
Completed shift from `requests` to `urllib` in v0_12.py.
- Implemented proper handling of non-JSON responses (like the root endpoint's "Ollama is running" message).
- Improved error handling for HTTP errors and URL errors.
- Fixed connection checking logic to work with Ollama's root endpoint.