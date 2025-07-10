import os, sys
from typing import Optional
import tkinter as tk
import tkinter.font

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

from Listeners import Listener
from Environment import UsageRecord, UserSetting
from .Styling import Styling

class ChatManager:
    """Manages chat interactions."""
    def __init__(self, master, desktop_koi, koi_menu):
        # Reference to main application and menu system
        self.master = master
        self.desktop_koi = desktop_koi
        self.koi_menu = koi_menu

        # Set up configuration
        self.user_setting = UserSetting()
        self.usage_record = UsageRecord()

        # Load settings
        model = str(self.user_setting.Get("chat_model"))
        api_type = str(self.user_setting.Get("chat_api_type"))
        host = str(self.user_setting.Get("chat_host"))
        port = self.user_setting.Get("chat_port")
        api_key: Optional[str] = None  # TODO
        version: Optional[str] = None

        self.listener = Listener(api_type, host, port, api_key, version)
        self.on_chat = False

        self.input_text = ""  # record input
        self.response = ""
        self.messages = []
        
        # Styling
        self.font = tkinter.font.Font(family=Styling.font_family, size=Styling.font_size)

    def listen_dialog(self) -> str:
        """Get input from user"""
        color_bg = Styling.color_background
        color_text = "#EEEEEE"

        dialog = tk.Toplevel(self.master)
        dialog.title("Listen")
        dialog.resizable(False, False)
        dialog.overrideredirect(True)
        dialog.attributes('-topmost', True)
        dialog.configure(bg='black')
        dialog.wm_attributes("-transparentcolor", "black")

        # Add text input box
        entry = tk.Text(dialog, bg=color_bg, fg=color_text, wrap="word", font=self.font)  # Apply styling font
        entry.pack(side=tk.TOP, padx=0, pady=0, expand=True, fill=tk.BOTH)  # Modified: Added expand and fill

        # Track input changes
        def update_size():
            """Update window size based on content"""
            dialog.update_idletasks()
            # Set max allowed width to 3x desktop_koi width
            max_width = self.desktop_koi.width * 3
            min_width = self.desktop_koi.width * 2

            self.input_text = entry.get("1.0", "end-1c")

            # Calculate required dimensions
            text = self.input_text + "中" # padding
            req_width = self.font.measure(text)

            # Limit width to min of required width, max allowed width, and 80% screen width
            screen_width = self.master.winfo_screenwidth()
            new_width = min(req_width, max_width, int(screen_width * 0.8))
            new_width = max(new_width, min_width)

            # Update dialog width and refresh layout to apply wrapping
            dialog.geometry(f"{new_width}x{dialog.winfo_height()}")  # Update width only
            dialog.update_idletasks()  # Force layout update

            # Now calculate the correct number of visible lines
            if self.input_text.strip():
                num_lines = self.font.measure(self.input_text) // (new_width - self.font.measure('0')) + 1
            else:
                num_lines = 1
            num_lines = min(num_lines, 5)
            
            line_height = self.font.metrics("linespace")
            new_height = max(1, num_lines) * line_height + 6

            dialog.geometry(f"{new_width}x{new_height}")
        
        def update_position():
            """Move with desktop_koi"""

        def on_send(dialog):
            """Handle send button click or Enter key press"""
            self.input_text = entry.get("1.0", tk.END).strip()
            if self.input_text:
                dialog.destroy()

        entry.bind("<KeyRelease>", lambda *args: update_size())
        entry.bind("<Return>", lambda e: on_send(dialog))

        # Position window relative to desktop_koi
        update_size()
        dialog.update_idletasks()
        x = self.desktop_koi.x + 10
        y = self.desktop_koi.y + self.desktop_koi.height + 10
        dialog.geometry(f"+{x}+{y}")

        # Wait for user input
        dialog.wait_window()
        return self.input_text

    def speak_dialog(self, text: str) -> None:
        """Display the response"""

    def Chat(self):
        """Chat with KOI"""
        if self.on_chat:
            return
        self.on_chat = True

        self.listen_dialog()
        
        prompt = self.input_text
        self.response = self.listener.Generate(prompt=prompt)

        self.input_text = ""
        self.on_chat = False