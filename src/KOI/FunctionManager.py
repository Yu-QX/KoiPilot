import sys, os, gc
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional
from Listeners import Listener
from FileManager.Counsellor import Counsellor
from FileManager.Operations import FileOperator, FolderOperator
from .Styling import Styling

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
    
    def confirmation_dialog(self, changes: Optional[dict] = None) -> list[bool]:
        """
        Displays a confirmation dialog window to the user.

        :param changes: A dictionary containing the changes to be confirmed. If not assigned, the function will use `self.changes`.
        :return: A list of booleans indicating whether the user confirmed each change.
        """
        if not changes:
            changes = self.changes
        confirmations: list[Optional[bool]] = [None for _ in changes]
        
        # Set up GUI
        root = tk.Tk()
        root.title("Confirm Changes")
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        root.configure(bg='black')
        root.wm_attributes("-transparentcolor", "black")

        color_bg = Styling.color_background

        confirm_window = tk.Canvas(root, bg="black", highlightthickness=0)
        confirm_window.pack(fill=tk.BOTH, expand=True)
        root.withdraw()

        # Create buttons
        line_list = []
        for idx, (original_name, suggested_name) in enumerate(changes.items()):
            # Create a frame for each line
            line_list.append(tk.Frame(confirm_window, bg=color_bg))
            line_list[idx].pack(fill=tk.X, padx=10, pady=5)
            # Add labels and buttons
            original_label = tk.Label(line_list[idx], text=original_name, bg=color_bg, fg="white", font=Styling.font_family)
            original_label.pack(side=tk.LEFT, padx=5)
            suggested_label = tk.Label(line_list[idx], text=suggested_name, bg=color_bg, fg="white", font=Styling.font_family)
            suggested_label.pack(side=tk.RIGHT, padx=5)

            # Define button commands using lambda to capture current index
            def confirm_command(idx):
                confirmations[idx] = True  # type: ignore
                line_list[idx].destroy()

            def cancel_command(idx):
                confirmations[idx] = False  # type: ignore
                line_list[idx].destroy()

            confirm_button = tk.Button(line_list[idx], text="Confirm", bg="green", fg="white", font=Styling.font_family, command=lambda i=idx: confirm_command(i))
            confirm_button.pack(side=tk.RIGHT, padx=5)
            cancel_button = tk.Button(line_list[idx], text="Cancel", bg="red", fg="white", font=Styling.font_family, command=lambda i=idx: cancel_command(i))
            cancel_button.pack(side=tk.RIGHT, padx=5)

        # Add "Confirm All" and "Cancel All" buttons at the bottom
        button_frame = tk.Frame(confirm_window, bg=color_bg)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        def confirm_all():
            for idx in range(len(confirmations)):
                if confirmations[idx] is None:
                    confirmations[idx] = True  # type: ignore
            root.quit()

        def cancel_all():
            for idx in range(len(confirmations)):
                if confirmations[idx] is None:
                    confirmations[idx] = False  # type: ignore
            root.quit()

        confirm_all_button = tk.Button(button_frame, text="Confirm All", bg="green", fg="white", font=Styling.font_family, command=confirm_all)
        confirm_all_button.pack(side=tk.LEFT, padx=5)
        cancel_all_button = tk.Button(button_frame, text="Cancel All", bg="red", fg="white", font=Styling.font_family, command=cancel_all)
        cancel_all_button.pack(side=tk.RIGHT, padx=5)

        # Start the main loop
        root.deiconify()
        root.mainloop()

        # Remove root and recycle memory
        root.destroy()
        del root
        gc.collect()
        
        # Filter out None values before returning
        return [value if value is not None else False for value in confirmations]

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
        files = FolderOperator.GetFiles(selected_folder)
        folders = FolderOperator.GetSubFolders(selected_folder)

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
        if not self.changes:
            messagebox.showinfo("No Changes", "No renaming suggestions were generated.")
            return

        # Get user confirmation with UI interaction
        confirm = self.confirmation_dialog()
        original_names = self.changes.keys()
        confirmed_changes = {}
        if len(confirm) != len(original_names):
            print("Error: Confirmation length does not match original names length.")
            return
        for original_name, confirmation in zip(original_names, confirm):
            if confirmation:
                confirmed_changes[original_name] = self.changes[original_name]

        # Implement confirmed suggestions
        for original_name, suggested_name in confirmed_changes.items():
            original_path = os.path.join(selected_folder, original_name)
            new_path = os.path.join(selected_folder, suggested_name)

            if os.path.isdir(original_path):
                result = FolderOperator.RenameFolder(original_path, new_path)
            else:
                result = FileOperator.RenameFile(original_path, new_path)

            if result != 210000:
                print(f"Failed to rename '{original_name}' to '{suggested_name}'. Error code: {result}")

        messagebox.showinfo("Success", "Renaming completed successfully.")