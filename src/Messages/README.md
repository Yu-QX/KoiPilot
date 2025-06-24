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
        "required_args": [
            "arg1",
            "arg2"
        ]  // This block will be used only if all required arguments are provided (optional)
    },
    "block 2": {
        "message": "Hello, {name}!"  // When `message_id` and `message` are both provided, `message` will be ignored.
    },  // blocks are lined up in order
    "block 3": {
        "message_id": "a/b/d",
        "dont_format": True  // Don't format the message. Use it if there is `{}` enclosing unexpected stuff in the message.
    }  // new line will be automaticly added between blocks
}
```