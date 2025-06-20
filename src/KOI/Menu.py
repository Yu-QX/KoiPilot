import tkinter as tk

class KOIMenu(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        
        # Configure window
        self.title("KOI Menu")
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.configure(bg='black')
        self.wm_attributes("-transparentcolor", "black")
        self.delay = 200
        self.color_menu = "#333333"
        self.color_outline = "#444444"
        self.radius = 15
        self.width = 100  # Default width
        self.height = 20  # Default height
        
        # Create a canvas for rounded rectangle background
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Define button list and create buttons
        self.buttons = []
        self.button_texts = ["Option 1", "Option 2", "Option 3"]
        for text in self.button_texts:
            btn = tk.Button(
                self.canvas, text=text, 
                command=lambda t=text: self.get_button_action(t)(), 
                bg=self.color_menu, fg='white', bd=0, highlightthickness=0
            )
            self.buttons.append(btn)

        # Layout buttons inside the canvas
        self.layout_buttons()

        # Hide menu initially
        self.withdraw()
        
    def get_button_action(self, text):
        if text == "Option 1":
            return self.option1_action
        elif text == "Option 2":
            return self.option2_action
        return lambda: None  # Default no-op action to prevent None return
    
    def option1_action(self):
        # Placeholder for option 1 functionality
        print("Option 1 selected")
        pass
    
    def option2_action(self):
        # Placeholder for option 2 functionality
        print("Option 2 clicked!")
        pass
    
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
            btn.place(relx=0.5, rely=(i + 0.5) / len(self.button_texts), anchor=tk.CENTER)

    def show(self):
        # Calculate position (centered relative to main window)
        master = self.master
        master.update_idletasks()  # Ensure we have current geometry values
        
        # Get master window properties
        master_x = master.winfo_x()
        master_y = master.winfo_y()
        master_width = master.winfo_width()
        master_height = master.winfo_height()
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
        self.master.after(self.delay, self.deiconify)

    def hide(self):
        self.master.after(self.delay, self.withdraw)