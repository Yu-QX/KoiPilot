import os, sys
from typing import Optional
import tkinter as tk
import tkinter.font
import tkinter.messagebox

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
        self.on_listen = False

        self.input_text = ""  # record input
        self.response = ""
        self.messages = []
        
        # Styling
        self.font = tkinter.font.Font(family=Styling.font_family, size=Styling.font_size)

        # Set up GUI
        self.setup_listen_dialog()
        self.setup_speak_dialog()

    def setup_listen_dialog(self):
        """Get input from user"""
        color_bg = Styling.color_background
        color_text = "#EEEEEE"

        self.listen_window = tk.Toplevel(self.master)
        self.listen_window.withdraw()
        self.listen_window.title("Listen")
        self.listen_window.resizable(False, False)
        self.listen_window.overrideredirect(True)
        self.listen_window.attributes('-topmost', True)
        self.listen_window.configure(bg='black')
        self.listen_window.wm_attributes("-transparentcolor", "black")

        # Add text input box
        self.entry = tk.Text(self.listen_window, bg=color_bg, fg=color_text, wrap="word", font=self.font)
        self.entry.pack(side=tk.TOP, padx=0, pady=0, expand=True, fill=tk.BOTH) 

        # Track input changes
        def update_size():
            """Update window size based on content"""
            self.listen_window.update_idletasks()
            # Set max allowed width to 3x desktop_koi width
            max_width = self.desktop_koi.width * 3
            min_width = self.desktop_koi.width * 2

            self.input_text = self.entry.get("1.0", tk.END).strip().replace("\n", " ")

            # Calculate required dimensions
            text = self.input_text + "中" # padding
            req_width = self.font.measure(text)

            # Limit width to min of required width, max allowed width, and 80% screen width
            screen_width = self.master.winfo_screenwidth()
            new_width = min(req_width, max_width, int(screen_width * 0.8))
            new_width = max(new_width, min_width)

            # Update self.listen_window width and refresh layout to apply wrapping
            self.listen_window.geometry(f"{new_width}x{self.listen_window.winfo_height()}")  # Update width only
            self.listen_window.update_idletasks()  # Force layout update

            # Now calculate the correct number of visible lines
            if self.input_text.strip():
                num_lines = self.font.measure(self.input_text) // (new_width - self.font.measure('0')) + 1
            else:
                num_lines = 1
            num_lines = min(num_lines, 5)
            
            line_height = self.font.metrics("linespace")
            new_height = (max(1, num_lines) + 1) * line_height

            self.listen_window.geometry(f"{new_width}x{new_height}")
            update_position()

        self.entry.bind("<KeyRelease>", lambda *args: update_size())

        # Send message
        def on_send():
            """Handle send button click or Enter key press"""
            input_text = self.entry.get("1.0", tk.END).strip().replace("\n", " ")
            if input_text:
                self.entry.delete("1.0", tk.END)
                if self.on_listen:
                    self.input_text = input_text
                    self.on_listen = False
                else:
                    tkinter.messagebox.showwarning("Warning", "Please wait for the previous message to finish processing.")
                    # Keep the entered text in the entry
                    self.entry.insert("1.0", input_text)
                    self.entry.mark_set(tk.INSERT, "1.end") 
                    self.entry.see("1.end") 
            else: pass

        self.entry.bind("<Return>", lambda e: on_send())

        # Bind to desktop_koi position changes
        def update_position():
            """Update dialog position relative to desktop_koi and ensure on-screen visibility"""
            self.listen_window.update_idletasks()

            dialog_width = self.listen_window.winfo_width()
            dialog_height = self.listen_window.winfo_height()

            # Calculate target position
            target_x = self.desktop_koi.x + (self.desktop_koi.width - dialog_width) // 2
            target_y = self.desktop_koi.y - dialog_height - 5
            
            # Get screen dimensions
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            
            # Get dialog dimensions
            dialog_width = self.listen_window.winfo_width()
            dialog_height = self.listen_window.winfo_height()
            
            # Adjust position to stay on screen
            final_x = min(target_x, screen_width - dialog_width - 10)
            final_y = min(target_y, screen_height - dialog_height - 10)
            
            # Apply position
            self.listen_window.geometry(f"+{final_x}+{final_y}")

        self.desktop_koi.root.bind("<Configure>", lambda e=None: update_size())
        update_size()

    def setup_speak_dialog(self):
        """Display the response"""
        color_bg = Styling.color_background
        color_text = "#EEEEEE"
        font = (Styling.font_family, Styling.font_size)

        self.speak_window = tk.Toplevel(self.master)
        self.speak_window.withdraw()
        self.speak_window.title("Speak")
        self.speak_window.resizable(False, False)
        self.speak_window.overrideredirect(True)
        self.speak_window.attributes('-topmost', True)
        self.speak_window.configure(bg='black')
        self.speak_window.wm_attributes("-transparentcolor", "black")

        # Create response display area
        self.response_label = tk.Label(
            self.speak_window,
            bg=color_bg,
            fg=color_text,
            font=font,
            wraplength=400,  # Initial wrap length
            justify=tk.LEFT,
            padx=10,
            pady=5
        )
        self.response_label.pack(padx=5, pady=5)

        # Update window size based on content
        def update_size():
            """Update window size based on response content"""
            self.speak_window.update_idletasks()
            
            # Calculate required dimensions
            text = self.response + "中"  # Add padding
            req_width = self.font.measure(text)
            
            # Limit width to 3x desktop_koi width or 80% screen width
            max_width = self.desktop_koi.width * 3
            screen_width = self.master.winfo_screenwidth()
            new_width = min(req_width, max_width, int(screen_width * 0.8))
            
            # Calculate lines and height
            if self.response.strip():
                num_lines = self.font.measure(self.response) // (new_width - self.font.measure('0')) + 1
            else:
                num_lines = 1
            num_lines = min(num_lines, 10)  # Max 10 lines
            
            line_height = self.font.metrics("linespace")
            new_height = (max(1, num_lines) + 2) * line_height
            
            # Update window dimensions
            self.speak_window.geometry(f"{new_width}x{new_height}")
            
            # Update label wrap length based on new width
            self.response_label.config(wraplength=new_width - 20)  # Subtract padding
            
            update_position()

        # Update response display
        def update_content():
            """Update response content and refresh display"""
            self.response_label.config(text=self.response)
            update_size()

        # Update dialog position relative to desktop_koi
        def update_position():
            """Update dialog position relative to desktop_koi and ensure on-screen visibility"""
            self.speak_window.update_idletasks()

            dialog_width = self.speak_window.winfo_width()
            dialog_height = self.speak_window.winfo_height()

            # Calculate target position
            target_x = self.desktop_koi.x + (self.desktop_koi.width - dialog_width) // 2
            target_y = self.desktop_koi.y + self.desktop_koi.height + 5
            
            # Get screen dimensions
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            
            # Adjust position to stay on screen
            final_x = min(target_x, screen_width - dialog_width - 10)
            final_y = min(target_y, screen_height - dialog_height - 10)
            
            # Apply position
            self.speak_window.geometry(f"+{final_x}+{final_y}")

        # Bind to desktop_koi position changes
        self.desktop_koi.root.bind("<Configure>", lambda e=None: update_position())
        
        # Store update method for external access
        self.update_speak_dialog = update_content

    def Chat(self):
        """Chat with KOI"""
        if self.on_chat:
            return
        self.on_chat = True
        self.listen_window.deiconify()

        while True:
            # Wait for user input
            self.on_listen = True
            while self.on_listen:
                # wait for user input
                self.master.update()
                    
            prompt = self.input_text
            self.input_text = ""
            self.response = self.listener.Generate(prompt=prompt)
            
            self.speak_window.deiconify()
            self.update_speak_dialog()
            self.speak_window.after(10000, self.speak_window.withdraw)
        
        self.on_chat = False