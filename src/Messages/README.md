# Description for `Messages` Module

The `Messages` module is designed to manage all messages used in the application, including system messages, AI prompts, and system error codes. It provides a centralized way to handle translations and dynamic message construction.

## Core Features

- **Message Retrieval**: Fetch messages based on IDs, supporting both JSON files and folder-based structures.
- **Dynamic Message Construction**: Construct complex messages using templates and arguments.
- **Language Support**: Automatically selects the preferred language based on user configurations.
- **Error Handling**: Provides descriptions for system codes and handles invalid inputs gracefully.

## How to Use

### 1. Initialize the Message Manager
To start using the module, initialize the `MessageManager` class.

### 2. Retrieve a Message
Use the `GetMessage` method to fetch a message by its ID:

```python
message_id = "Prompts/FileToFolder/1"
message = manager.GetMessage(message_id)
print(message)
```

### 3. Construct a Message
Use the `Construct` method to dynamically build messages with placeholders:

```python
template_id = "Prompts/FileToFolder"
args = {"file": "example.txt", "folder_options": ["Documents", "Images"]}
constructed_message = manager.Construct(template_id, **args)
print(constructed_message)
```

### 4. Get System Code Description
Retrieve the description of a system code using the [SystemCode](file://d:\CodeHub\KoiPilot\src\Messages\__init__.py#L197-L207) method:

```python
code = 210100
description = manager.SystemCode(code)
print(description)
```

## Language Support

The module supports multiple languages, with a priority order defined in the configuration. The default priority is:

```python
self.LanguagePriorities = ["EN", "CN"]
```

If a file or JSON entry does not exist for the preferred language, the next available language in the list will be used.

## Error Handling

The module includes robust error handling:
- If a message ID points to an invalid path, an empty string is returned.
- JSON decoding errors are caught and logged.
- Missing system codes return a default message: `"Unknown System Code"`.

## Example Directory Structure

### JSON Mode
A JSON file contains translations for different languages:

```json
{
    "EN": "Hello!",
    "CN": "你好!"
}
```

### Folder Mode
A folder contains files named after supported languages:

```
TargetFolder/
├── EN.md
└── CN.md
```

## Additional Notes

For more details on template structure and usage, refer to the inline comments in the [`__init__.py`](__init__.py) file.