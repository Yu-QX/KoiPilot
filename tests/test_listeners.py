import os
import sys

# Add the 'src' directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Listeners import Listener

def main():
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

if __name__ == "__main__":
    main()