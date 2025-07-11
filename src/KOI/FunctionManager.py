import sys, os, gc
import threading
import tkinter as tk
from typing import Optional
from tkinter import filedialog, messagebox

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

from Environment import Logger
from Environment import UserSetting, UsageRecord
from Listeners import Listener
from FileManager.Counsellor import Counsellor
from FileManager.Operations import FileOperator, FolderOperator
from .Styling import Styling

class FunctionManager:
    """Handles all the functions for KOI to call."""
    def __init__(self, master, desktop_koi, koi_menu):
        # Reference to main application and menu system
        self.master = master
        self.desktop_koi = desktop_koi  
        self.koi_menu = koi_menu 

        # Set up configuration
        self.user_setting = UserSetting()
        self.usage_record = UsageRecord()
        
        # Load settings
        model = str(self.user_setting.Get("function_model"))
        api_type = str(self.user_setting.Get("function_api_type"))
        host = str(self.user_setting.Get("function_host"))
        port = self.user_setting.Get("function_port")
        api_key: Optional[str] = None  # TODO
        version: Optional[str] = None
        
        self.on_task_format_names = False
        self.on_task_sort_files = False

        self.counsellor = Counsellor(model, api_type, host, port, api_key, version)
        #self.listener = Listener(api_type, host, port, api_key, version)

    def confirmation_dialog(self, changes: Optional[dict] = None) -> list[bool]:
        """
        Displays a confirmation dialog window to the user.
        
        :param changes: A dictionary containing the changes to be confirmed. If not assigned, the function will use `self.changes`.
        :return: A list of booleans indicating whether the user confirmed each change.
        """
        if not changes:
            changes = self.changes
        confirmations: list[Optional[bool]] = [None for _ in changes]
        
        color_bg = Styling.color_background
        
        # Set up GUI
        dialog = tk.Toplevel(self.master)
        dialog.title("Confirm Changes")
        dialog.configure(bg='black')
        dialog.attributes('-topmost', True)
        dialog.resizable(False, False)  # Forbid resizing
        dialog.withdraw()

        # Create main container frame (will hold both scrollable area and buttons)
        main_container = tk.Frame(dialog, bg=color_bg)
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)

        # Create scrollable frame with canvas and scrollbar
        canvas_frame = tk.Frame(main_container, bg=color_bg)
        canvas_frame.grid(row=0, column=0, sticky="nsew")

        canvas = tk.Canvas(canvas_frame, bg='black', highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=color_bg)

        # Store screen dimensions
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable content
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Create pinned buttons container (separate from scrollable content)
        button_frame = tk.Frame(main_container, bg=color_bg)
        button_frame.grid(row=1, column=0, sticky="ew")

        # Create content lines
        line_list = []
        max_line_width = 0  # Track maximum line width

        def adjust_dialog_size():
            nonlocal max_line_width
            
            remaining_lines = [line for line in line_list if line.winfo_exists()]
            if not remaining_lines:
                return 0

            # Calculate new dimensions
            new_scroll_height = sum(line.winfo_height() for line in remaining_lines)
            new_scroll_height += 2 * 5 * len(remaining_lines)  # Padding
            
            # Update max width if needed
            current_max_width = max(line.winfo_reqwidth() for line in remaining_lines) if remaining_lines else max_line_width
            max_line_width = max(max_line_width, current_max_width)
            
            # Calculate total window height (scroll area + buttons)
            button_height = button_frame.winfo_reqheight()
            new_window_height = min(new_scroll_height + button_height + 10, screen_height // 2)
            
            # Determine if we need scrollbar
            needs_scrollbar = (new_scroll_height + button_height) > (screen_height // 2)
            
            if needs_scrollbar:
                # Constrain scrollable area height
                scrollable_height = new_window_height - button_height - 10
                canvas.config(height=scrollable_height)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                # Hide scrollbar when not needed
                scrollbar.pack_forget()
                canvas.config(height=new_scroll_height)
            
            # Set fixed width for all components
            canvas.config(width=max_line_width)
            scrollable_frame.config(width=max_line_width)
            for line in remaining_lines:
                line.config(width=max_line_width)
            
            # Update geometry
            dialog.geometry(f"{int(max_line_width + (20 if needs_scrollbar else 0))}x{int(new_window_height)}")
            
            return new_window_height

        for idx, (original_name, suggested_name) in enumerate(changes.items()):
            # Create a frame for each line
            line_frame = tk.Frame(scrollable_frame, bg=color_bg)
            line_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Add labels and buttons
            original_label = tk.Label(line_frame, text=original_name, bg=color_bg, fg="white", font=Styling.font_family)
            original_label.pack(side=tk.LEFT, padx=5)
            arrow = tk.Label(line_frame, text="->", bg=color_bg, fg="red", font=Styling.font_family)
            arrow.pack(side=tk.LEFT, padx=5)
            suggested_label = tk.Label(line_frame, text=suggested_name, bg=color_bg, fg="white", font=Styling.font_family)
            suggested_label.pack(side=tk.LEFT, padx=5)

            # Button commands
            def confirm_command(idx):
                confirmations[idx] = True
                line_list[idx].destroy()
                adjust_dialog_size()
                if not None in confirmations:
                    dialog.destroy()

            def cancel_command(idx):
                confirmations[idx] = False
                line_list[idx].destroy()
                adjust_dialog_size()
                if not None in confirmations:
                    dialog.destroy()

            confirm_button = tk.Button(line_frame, text="Confirm", bg="green", fg="white", 
                                font=Styling.font_family, command=lambda i=idx: confirm_command(i))
            confirm_button.pack(side=tk.RIGHT, padx=5)
            cancel_button = tk.Button(line_frame, text="Cancel", bg="red", fg="white", 
                                font=Styling.font_family, command=lambda i=idx: cancel_command(i))
            cancel_button.pack(side=tk.RIGHT, padx=5)

            line_list.append(line_frame)

        # Add "Confirm All" and "Cancel All" buttons
        def confirm_all():
            for idx in range(len(confirmations)):
                if confirmations[idx] is None:
                    confirmations[idx] = True
            dialog.destroy()

        def cancel_all():
            for idx in range(len(confirmations)):
                if confirmations[idx] is None:
                    confirmations[idx] = False
            dialog.destroy()

        confirm_all_button = tk.Button(button_frame, text="Confirm All", bg="green", fg="white", 
                                font=Styling.font_family, command=confirm_all)
        confirm_all_button.pack(side=tk.LEFT, padx=5)
        cancel_all_button = tk.Button(button_frame, text="Cancel All", bg="red", fg="white", 
                                font=Styling.font_family, command=cancel_all)
        cancel_all_button.pack(side=tk.RIGHT, padx=5)

        # Initial size calculation
        dialog.update_idletasks()
        adjust_dialog_size()

        # Center window calculation
        dialog.update_idletasks()
        x = (screen_width - dialog.winfo_width()) // 2
        y = (screen_height - dialog.winfo_height()) // 3  # Position upper third

        # Set final position
        dialog.geometry(f"+{int(x)}+{int(y)}")
        
        # Start dialog
        dialog.deiconify()
        self.master.wait_window(dialog)
        
        return [value if value is not None else False for value in confirmations]

    def FormatNames(self):
        """Format the names of files and folders in selected folder."""
        if self.on_task_format_names:
            messagebox.showwarning("Warning", "A task is already running.")
            return
        self.on_task_format_names = True

        # Get the selected folder with UI interaction
        selected_folder = filedialog.askdirectory(title="Select Folder to Format Names")  # TODO: Message
        if not selected_folder:
            messagebox.showinfo("No Folder Selected", "You did not select a folder.")
            self.on_task_format_names = False
            return  # Exit if no folder is selected

        # Get the names of files and folders in the selected folder
        files = FolderOperator.GetFiles(selected_folder)
        folders = FolderOperator.GetSubFolders(selected_folder)

        # Generate suggestions, and save the suggestions in local variable
        if len(files) >= 3:
            file_changes = self.counsellor.FormatFileNames(files)
        else:
            file_changes = {}
        if len(folders) >= 3:
            folder_changes = self.counsellor.FormatFileNames(folders)
        else:
            folder_changes = {}
        self.changes = {**file_changes, **folder_changes}
        if not self.changes:
            messagebox.showinfo("No Changes", "No renaming suggestions were generated.")
            self.on_task_format_names = False
            return

        # Get user confirmation with UI interaction
        confirm = self.confirmation_dialog()
        original_names = self.changes.keys()
        confirmed_changes = {}
        if len(confirm) != len(original_names):
            print("Error: Confirmation length does not match original names length.")
            self.on_task_format_names = False
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
        self.on_task_format_names = False
        return
    
    def SortFiles(self):
        """Place files into appropriate folders."""
        if self.on_task_sort_files:
            messagebox.showwarning("Warning", "A task is already running.")
            return
        self.on_task_sort_files = True

        # Get the folder containing all the files to be sorted with UI interaction
        source_folder = filedialog.askdirectory(title="Select Folder to Sort")
        if not source_folder:
            messagebox.showinfo("No Folder Selected", "You did not select a folder.")
            self.on_task_sort_files = False
            return
        
        # Get the options of folder to sort into with UI interaction
        destination_folder = filedialog.askdirectory(title="Select Folder to Sort Into (this will include all subfolders)")
        if not destination_folder:
            messagebox.showinfo("No Folder Selected", "You did not select a folder.")
            self.on_task_sort_files = False
            return
        
        # Get all the subfolders in the destination folder, and the files in the source folder
        option_folder = FolderOperator.GetSubFolders(destination_folder)  # TODO: folder tree
        files = FolderOperator.GetFiles(source_folder)

        # Generate suggestions, and save the suggestions in local variable
        self.changes = {}
        threads = []
        local_changes = {}

        for file in files:
            thread = threading.Thread(target=self._move_to_folder_thread, args=(file, option_folder, local_changes))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        self.changes.update(local_changes)

        if not self.changes:
            messagebox.showinfo("No Changes", "No moving suggestions were generated.")
            self.on_task_sort_files = False
            return

        # Get user confirmation with UI interaction
        confirm = self.confirmation_dialog()
        original_files = self.changes.keys()
        confirmed_changes = {}
        if len(confirm) != len(original_files):
            print("Error: Confirmation length does not match original files length.")
            self.on_task_sort_files = False
            return
        for original_file, confirmation in zip(original_files, confirm):
            if confirmation:
                confirmed_changes[original_file] = self.changes[original_file]

        # Implement confirmed suggestions
        for file_to_move, target_folder in confirmed_changes.items():
            source_path = os.path.join(source_folder, file_to_move)
            destination_path = os.path.join(destination_folder, target_folder)
            
            # Move the file
            result = FileOperator.MoveFile(source_path, destination_path)
            if result != 210000:
                print(f"Failed to move '{file_to_move}' to '{target_folder}'. Error code: {result}")

        messagebox.showinfo("Success", "Sorting completed successfully.")
        self.on_task_sort_files = False

    def _move_to_folder_thread(self, file, option_folder, local_changes):
        """Helper method to run in a separate thread."""
        suggestion = self.counsellor.MoveToFolder(file, option_folder)
        if suggestion:
            local_changes[file] = suggestion
        return