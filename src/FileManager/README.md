# Description for `FileManager` Module

The `FileManager` module provides a set of functions for managing files and directories. Including:
- [ ] Classify and organize
- [ ] Search and locate
- [ ] Batch rename/move/remove
- [ ] Add tags and write notes

---

## File `Operations.py`

The file `Operations.py` provides functions for operating with files and folders.

It also contains security checks to prevent unauthorized access.

### Class `FileOperator`

The `FileOperator` class provides methods for operating with files. 

Functions in `FileOperator`:
- `RenameFile(old_name, new_name)`
- `MoveFile(file_path, destination_folder)`
- `RemoveFile(file_path)`

### Class `FolderOperator`

The `FolderOperator` class provides methods for operating with folders.

Functions in `FolderOperator`:
- `CreateFolder(folder_path, exist_ok=False)`

---

## FIle `Counsellor.py`

### Class `Counsellor`

The `Counsellor` class provides AI assistance for file operations. It uses the `Listeners` module to interact with AI APIs. In this class, only suggestions are provided by the AI, and the user has the final say in the file operations.
