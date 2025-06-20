import tkinter as tk
from typing import Optional
from .FunctionManager import FunctionManager

# Developer Note: 
# - `CamelCase` for variables and functions to export and `snake_case` for internal use 

class KOIMenu(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        
        # Configure window
        self.title("KOI Menu")
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.configure(bg='black')
        self.wm_attributes("-transparentcolor", "black")
        self.duration_fade = 200  # The duration of the fade in ms
        self.delay = 100
        self.color_menu = "#333333"
        self.color_outline = "#444444"
        self.color_text = "#FFFFFF"
        self.color_target = "#666666"
        self.radius = 15
        self.width = 100  # Default width
        self.height = 20  # Default height

        # Create a canvas for rounded rectangle background
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.menu_visible = False

        # Define button list and create buttons
        self.buttons = []
        self.button_list = {
            "Sort Files": self.button_relocate_files,
            "Format Names": self.button_format_filenames,
            "Chat": self.button_chat,
        }  # TODO: Import `Messages` module
        for text, action in self.button_list.items():
            btn = tk.Button(
                self.canvas, text=text, 
                command=action if action else lambda: None, 
                bg=self.color_menu, fg=self.color_text, 
                bd=0, highlightthickness=0
            )

            # Bind hover effects
            #btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.color_target, fg="#00FF00"))
            #btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.color_menu, fg=self.color_text))
            
            self.buttons.append(btn)
        self.layout_buttons()

        # Hide menu initially
        self.withdraw()
        self.function_manager = FunctionManager()

    def layout_buttons(self):
        # Dynamically adjust width and height based on button count
        num_buttons = len(self.buttons)
        #self.width = max(100, num_buttons * 50)  # Minimum width of 100 # TODO: Calculate based on button text length
        self.height = max(30, num_buttons * 30)  # Minimum height of 20

        # Draw rounded rectangle on canvas
        x1, y1, x2, y2, radius = 0, 0, self.width, self.height, self.radius
        self.canvas.create_oval(x1, y1, x1 + radius * 2, y1 + radius * 2, fill=self.color_menu, outline=self.color_menu)  # Top-left corner
        self.canvas.create_oval(x2 - radius * 2, y1, x2, y1 + radius * 2, fill=self.color_menu, outline=self.color_menu)  # Top-right corner
        self.canvas.create_oval(x1, y2 - radius * 2, x1 + radius * 2, y2, fill=self.color_menu, outline=self.color_menu)  # Bottom-left corner
        self.canvas.create_oval(x2 - radius * 2, y2 - radius * 2, x2, y2, fill=self.color_menu, outline=self.color_menu)  # Bottom-right corner
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=self.color_menu, outline=self.color_menu)
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=self.color_menu, outline=self.color_menu)

        # Place buttons inside the rounded rectangle
        for i, btn in enumerate(self.buttons):
            btn.place(relx=0.5, rely=(i + 0.5) / len(self.button_list), anchor=tk.CENTER)

    def Show(self, event: Optional[tk.Event] = None):
        """Show the menu with a fade-in effect"""
        if self.menu_visible or getattr(self.master, 'on_drag', False):
            return
        self.menu_visible = True

        # Calculate position (centered relative to main window)
        master = self.master
        master.update_idletasks()  # Ensure we have current geometry values

        # Get master window properties
        master_x = master.winfo_x()
        master_y = master.winfo_y()
        master_width = master.winfo_width()
        center_x = int(master_x + (master_width / 2))
        center_y = int(master_y)

        menu_width = self.width  # Use dynamically calculated width
        menu_height = self.height  # Use dynamically calculated height
        post_x = center_x - (menu_width // 2)
        post_y = center_y - menu_height

        # Record position
        self.x1, self.y1 = post_x, post_y
        self.x2, self.y2 = post_x + menu_width, post_y + menu_height

        # Position window
        self.geometry(f"{menu_width}x{menu_height}+{post_x}+{post_y}")
        
        # Start from hidden state; Gradually increase alpha using duration_fade
        self.attributes("-alpha", 0.0)
        self.deiconify()
        steps = 10
        step_delay = self.duration_fade // steps
        for i in range(1, steps + 1):
            self.after(i * step_delay, lambda a=i / steps: self.attributes("-alpha", a))

    def Hide(self, event: Optional[tk.Event] = None):
        """Hide the menu with a fade-out effect"""
        if not self.menu_visible:
            return
        self.menu_visible = False
        
        # Gradually decrease alpha using duration_fade
        steps = 10
        step_delay = self.duration_fade // steps
        for i in range(steps, -1, -1):
            self.after((steps - i) * step_delay, lambda a=i / steps: self.attributes("-alpha", a))

        # After fading out, withdraw the window
        self.after(self.duration_fade, self.withdraw)
    
    def button_chat(self):
        """Activate chat mode"""
        self.Hide()
        # TODO: Implement chat mode
    
    def button_relocate_files(self):
        """Choose files to relocate to different folders using AI"""
        self.Hide()
        # TODO: Implement relocate files mode
    
    def button_format_filenames(self):
        """Format filenames in a folder using AI"""
        self.Hide()
        self.master.after(0, self.function_manager.FormatName)