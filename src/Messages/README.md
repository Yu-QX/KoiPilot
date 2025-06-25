# Description for `Messages` Module

The `Messages` module with `MessageManager` class holds all the messages used in the app. Including:
- system messages
- AI prompts
- system error codes

It also provide translations for all messages.

All messages are stored in the module. 

## `GetMessage` Attribute

The `GetMessage` attribute is used to get a message of the ID from the module. The input `message_id` will be converted to a path. If it points to a `JSON` file (no suffix needed in passing in), the file will be loaded to find message in the preferred language; if it is a folder, accepted files with name of different languages in the folder will be searched.

In `JSON` mode:

```json
// TargetFile.json
{
    "EN": "Hello!",
    "CN": "你好!"
}
```

In `Folder` mode:

```txt
TargetFolder/
├── EN.md
└── CN.md
```

## `Construct` Attribute

The `Construct` attribute is used to construct messages with given templates and other arguments. It can decide on which message to use based on offered arguments. The ID must point to a `JSON`.

Example template `JSON`:

```json
{
    "block 1": {
        "message_id": "a/b/c",  // Use ID for message (recommended method)
    },  // The block will be used only if all required arguments are provided.
    "block 2": {
        "message": "Hello, {name}!",  // When `message_id` and `message` are both provided, `message` will be ignored.
        "case": [
            "requirement 1",
            "requirement 2",  // When passing in a string, check arguments and convert to boolean.
            {"requirement 3": "value"}  // When passing in a dict, check if the arguments match.
        ]  // The block will be used only if all requirements are met. Can also used a single string or dictionary. (Optional)
    },  // blocks are lined up in order.
    "block 3": {
        "message_id": "a/b/d",
        "dont_format": true  // Don't format the message. Use it if there is `{}` enclosing unexpected stuff in the message.
    },  // New line will be automaticly added between blocks. You can also specify with `join_with`.
    "RESPONSE_FORMAT": {
        "result": "folder",
        "reason": "reason"
    }  // Capitals are reserved for special functions. `RESPONSE_FORMAT` indicates the AI response format.
}
```