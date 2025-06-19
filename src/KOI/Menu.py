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
        self.delay_animation = 200
        
        # Create menu items
        self.option1 = tk.Button(self, text="Option 1", command=self.option1_action)
        self.option2 = tk.Button(self, text="Option 2", command=self.option2_action)
        
        # Layout
        self.option1.pack(pady=5)
        self.option2.pack(pady=5)

        # Hide menu
        self.withdraw()
        
    def option1_action(self):
        # Placeholder for option 1 functionality
        print("Option 1 selected")
        pass
    
    def option2_action(self):
        # Placeholder for option 2 functionality
        print("Option 2 clicked!")
        pass
    
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
        menu_width = 120  # Approximate width based on buttons
        menu_height = 70  # Approximate height based on buttons
        post_x = center_x - (menu_width // 2)
        post_y = center_y - menu_height
 
        # Record position
        self.x1, self.y1 = post_x, post_y
        self.x2, self.y2 = post_x + menu_width, post_y + menu_height
        
        # Position window
        self.geometry(f"{menu_width}x{menu_height}+{post_x}+{post_y}")
        self.master.after(self.delay_animation, self.deiconify)

    def hide(self):
        self.master.after(self.delay_animation, self.withdraw)