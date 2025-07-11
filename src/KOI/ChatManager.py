import os, sys
import time, json, re
import threading
from typing import Optional
import tkinter as tk
import tkinter.font
import tkinter.messagebox

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

from Listeners import Listener
from Environment import UsageRecord, UserSetting
from Environment import CHAT_HISTORY_FILE, CHAT_HISTORY_PATH
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
        self.listener.SetModel(model)
        self.on_chat = False
        self.on_listen = False
        self.on_generate = False

        self.input_text = ""  # record input
        self.output_text = ""
        self.response = ""
        self.max_dialog = 10
        self.history = []
        
        # Styling
        self.font = tkinter.font.Font(family=Styling.font_family, size=Styling.font_size)

        # Set up GUI
        self.load_chat_history()
        self.setup_speak_dialog()
        self.setup_listen_dialog()
        self.update_position()
        
        self.desktop_koi.root.bind("<Configure>", lambda e=None: self.update_position())

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
            self.update_position()

        self.entry.bind("<KeyRelease>", lambda *args: update_size())

        # Send message
        def on_send():
            """Handle send button click or Enter key press"""
            input_text = self.entry.get("1.0", tk.END).strip().replace("\n", " ")
            if input_text:
                self.entry.delete("1.0", tk.END)
                if self.on_listen:
                    self.input_text = input_text
                    self.speak_window.withdraw()
                    self.on_listen = False
                else:
                    tkinter.messagebox.showwarning("Warning", "Please wait for the previous message to finish processing.")
                    # Keep the entered text in the entry
                    self.entry.insert("1.0", input_text)
                    self.entry.mark_set(tk.INSERT, "1.end") 
                    self.entry.see("1.end") 
            else: pass

        self.entry.bind("<Return>", lambda e: on_send())
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

        # Create response display area with scroll support
        self.response_frame = tk.Frame(self.speak_window)
        self.response_frame.pack(fill=tk.BOTH, expand=True)

        self.response_label = tk.Text(
            self.response_frame,
            bg=color_bg,
            fg=color_text,
            font=font,
            wrap="word",
            borderwidth=0,
            highlightthickness=0,
            state=tk.DISABLED
        )
        self.response_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.response_frame, command=self.response_label.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.response_label.config(yscrollcommand=self.scrollbar.set)

    def update_speak_content(self):
        """Update response content and refresh display"""
        # Clear existing content
        self.response_label.config(state=tk.NORMAL)
        self.response_label.delete("1.0", tk.END)
        self.response_label.insert("1.0", self.output_text)
        self.response_label.config(state=tk.DISABLED)
        
        # Update layout to calculate new dimensions
        self.speak_window.update_idletasks()
        
        # Apply size constraints
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        max_width = min(4 * self.desktop_koi.width, int(screen_width * 0.8))
        max_height = int(screen_height * 0.5)

        # calculate new dimensions
        linespace = self.font.metrics("linespace")
        length = self.font.measure(self.output_text)
        text_area = linespace * length * 1.3

        new_height = linespace + 5
        new_width = 10
        self.speak_window.geometry(f"{new_width}x{new_height}")
        self.update_position()

        while True:
            self.speak_window.update_idletasks()
            if text_area > new_width * new_height:
                if new_width < max_width:
                    new_width += 10
                elif new_height < max_height:
                    new_height += linespace
                else:
                    break
            else:
                break    
            self.speak_window.geometry(f"{new_width}x{new_height}")
            self.update_position()
    
        self.update_position()

    def update_position(self):
        """Update dialog position relative to desktop_koi and ensure on-screen visibility"""
        self.listen_window.update_idletasks()
        self.speak_window.update_idletasks()

        listen_dialog_width = self.listen_window.winfo_width()
        listen_dialog_height = self.listen_window.winfo_height()
        speak_dialog_width = self.speak_window.winfo_width()
        speak_dialog_height = self.speak_window.winfo_height()

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        margin_width = 5
        space_koi_listen = 10
        space_listen_speak = 5

        # Calculate target positions
        # listen_window: above desktop_koi with 10px margin
        listen_target_x = self.desktop_koi.x + (self.desktop_koi.width - listen_dialog_width) // 2
        listen_target_y = self.desktop_koi.y - listen_dialog_height - space_koi_listen

        # speak_window: above listen_window with 5px margin
        speak_target_x = self.desktop_koi.x + (self.desktop_koi.width - speak_dialog_width) // 2
        speak_target_y = listen_target_y - speak_dialog_height - space_listen_speak

        # Adjust positions to stay on screen
        # adjust x
        listen_final_x = min(listen_target_x, screen_width - listen_dialog_width - margin_width)
        listen_final_x = max(listen_final_x, margin_width)
        speak_final_x = min(speak_target_x, screen_width - speak_dialog_width - margin_width)
        speak_final_x = max(speak_final_x, margin_width)
        
        # adjust y
        listen_final_y = listen_target_y
        speak_final_y = speak_target_y
        # if the speak_window is visible and it is off-screen
        if speak_final_y < margin_width and self.speak_window.winfo_ismapped():
            speak_final_y = margin_width
            listen_final_y = speak_final_y + speak_dialog_height + space_listen_speak
            # relocate desktop_koi
            self.desktop_koi.y = listen_final_y + listen_dialog_height + space_koi_listen
            self.desktop_koi.root.geometry(f"+{self.desktop_koi.x}+{self.desktop_koi.y}")
        elif listen_final_y < margin_width and not self.speak_window.winfo_ismapped() and self.listen_window.winfo_ismapped():
            listen_final_y = margin_width
            # relocate desktop_koi
            self.desktop_koi.y = listen_final_y + listen_dialog_height + space_koi_listen
            self.desktop_koi.root.geometry(f"+{self.desktop_koi.x}+{self.desktop_koi.y}")

        # Apply positions
        self.listen_window.geometry(f"+{listen_final_x}+{listen_final_y}")
        self.speak_window.geometry(f"+{speak_final_x}+{speak_final_y}")

    def load_chat_history(self):
        """Load chat history from JSON file or create new file if not exists"""
        try:
            if not os.path.exists(CHAT_HISTORY_PATH):
                os.makedirs(CHAT_HISTORY_PATH)
            
            if os.path.exists(CHAT_HISTORY_FILE):
                with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=2)
        except Exception as e:
            print(f"Error loading chat history: {e}")
            self.history = []

    def save_chat_history(self):
        """Save current chat history to JSON file"""
        try:
            with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving chat history: {e}")

    def process_response(self) -> str:
        """Process KOI's response"""
        result = self.response

        # Remove <think> tags and their content (including newlines)
        result = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL)

        self.output_text = result.strip()
        return self.output_text
    
    def Chat(self):
        """Chat with KOI"""
        if self.on_chat:
            return
        self.on_chat = True

        self.listen_window.deiconify()
        self.update_position()
        self.koi_menu.Buttons({
            "Exit Chat": lambda: setattr(self, 'on_chat', False)
        })

        def generate_response_async(prompt):
            self.on_generate = True
            self.response = self.listener.Generate(prompt=prompt)
            self.on_generate = False

        while self.on_chat:
            # Wait for user input
            self.on_listen = True
            while self.on_listen and self.on_chat:
                # wait for user input
                try:
                    self.master.update()
                except RuntimeError:
                    print("Main thread terminated")
                    self.on_chat = False
                    return
            if not self.on_chat:
                break

            user_input = self.input_text
            prompt = user_input # TODO
            print(prompt)

            # Start response generation in a background thread
            threading.Thread(target=generate_response_async, args=(prompt,)).start()
            threading.Thread(target=self.desktop_koi.Animate).start()
            self.input_text = ""
            self.on_generate = True
            while self.on_chat and self.on_generate:
                try:
                    self.master.update()
                except RuntimeError:
                    print("Main thread terminated")
                    self.on_chat = False
                    return
            if not self.on_chat:
                break
            
            self.process_response()
            current_entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "user_input": user_input,
                "koi_output": self.output_text,
                "prompt": prompt,
                "response": self.response,
            }
            self.history.append(current_entry)
            self.save_chat_history()

            self.speak_window.deiconify()
            self.update_speak_content()
        
        self.speak_window.withdraw()
        self.listen_window.withdraw()        
        self.koi_menu.Buttons()
        self.on_chat = False