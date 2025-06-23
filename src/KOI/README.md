# Description for `KOI` Module

This is the main module of the KoiPilot app. It contains the core logic and functionality of the app, and builds up the interface.

---

## `KOI` Module Composition

### `KOI.py`

The entry point of the app.

### `Menu.py`

The menu interface of the app.

### `AnimationLoader.py`

Load the animation files of a *KOI*. Called in `KOI.py`.

Note that this module is only responsible for loading the animation files and their descriptions, and does not contain playing. It is seperated to allow for more flexibility in the future.

### `FunctionManager.py`

Handles the functions of KOI. Called in `Menu.py`.

---

## Modules Construction
The construction of the *KoiPilot* app is as follows:

**Functional modules include:**
- `FileManager`: A module that provides functions for managing files and directories.

**Support modules include:**
- `Listeners`: A module that holds all the AI APIs.
- `Massages`: A module that holds all the messages used in the app.

For more details, please refer to the corresponding module documentation in `README.md` of each module.
