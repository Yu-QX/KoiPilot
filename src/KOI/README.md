# Description for `KOI` Module

This is the main module of the KoiPilot project. It contains the core logic and functionality of the program, and builds up the interface.

---

## `KOI` Module Composition

### `KOI.py`

The entry point of the program.

### `AnimationLoader.py`

Load the animation files of a *KOI*.

Note that this module is only responsible for loading the animation files and their descriptions, and does not contain playing. It is seperated to allow for more flexibility in the future.

---

## Modules Construction
The construction of the *KoiPilot* project is as follows:

**Functional modules include:**
- `FileManager`: A module that provides functions for managing files and directories.

**Support modules include:**
- `Listeners`: A module that holds all the AI APIs.
- `Massages`: A module that holds all the messages used in the program.

For more details, please refer to the corresponding module documentation in `README.md` of each module.
