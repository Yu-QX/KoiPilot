import sys, os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional
from FileManager.Counsellor import Counsellor
from FileManager.Operations import FileOperator, FolderOperator
from Listeners import Listener

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

class FunctionManager:
    """Handles all the functions for KOI to call."""
    def __init__(self):
        # TODO: Auto load from config file
        model: Optional[str] = "qwen3:0.6B" # change it to your model
        api_type: str = "ollama"
        host: str = "localhost"
        port: Optional[int] = None
        api_key: Optional[str] = None
        version: Optional[str] = None

        self.counsellor = Counsellor(model, api_type, host, port, api_key, version)
        self.listener = Listener(api_type, host, port, api_key, version)
    
    def FormatName(self):
        """Format the names of files and folders in selected folder."""
        # Get the selected folder with UI interaction
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        selected_folder = filedialog.askdirectory(title="Select Folder to Format Names")  # TODO: Message
        if not selected_folder:
            messagebox.showinfo("No Folder Selected", "You did not select a folder.")
            return  # Exit if no folder is selected

        # Get the names of files and folders in the selected folder
        try:
            files = FolderOperator.GetFiles(selected_folder)
            folders = FolderOperator.GetSubFolders(selected_folder)
        except (FileNotFoundError, NotADirectoryError) as e:
            print(f"Error: {e}")
            return

        # Generate suggestions, and save the suggestions in local variable
        if len(files) >= 3:
            file_changes = self.counsellor.FormatName(files)
        else:
            file_changes = {}
        if len(folders) >= 3:
            folder_changes = self.counsellor.FormatName(folders)
        else:
            folder_changes = {}
        self.changes = {**file_changes, **folder_changes}

        # Get user confirmation with UI interaction
        if not self.changes:
            messagebox.showinfo("No Changes", "No renaming suggestions were generated.")
            return

        confirmation_message = "\n".join([f"{original} -> {new}" for original, new in self.changes.items()])
        confirm = messagebox.askyesno("Confirm Renaming", f"Apply the following changes?\n\n{confirmation_message}")
        if not confirm:
            return

        # Implement confirmed suggestions
        for original_name, suggested_name in self.changes.items():
            original_path = os.path.join(selected_folder, original_name)
            new_path = os.path.join(selected_folder, suggested_name)

            if os.path.isdir(original_path):
                result = FolderOperator.RenameFolder(original_path, new_path)
            else:
                result = FileOperator.RenameFile(original_path, new_path)

            if result != 210000:
                print(f"Failed to rename '{original_name}' to '{suggested_name}'. Error code: {result}")

        messagebox.showinfo("Success", "Renaming completed successfully.")