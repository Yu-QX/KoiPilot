import os
from typing import Optional
import tkinter as tk
from .AnimationLoader import AnimationLoader

class DesktopKOI:
    """The main class for the KOI"""
    def __init__(self, root):
        self.root = root

        # Define KOI variables
        self.mood = "standard"

        # Launch window
        self.load_animations()  # TODO: remember the location when last used
        self.setup_gui()

        # Bind events for dragging
        self.start_x = 0
        self.start_y = 0
        self.root.bind("<ButtonPress-1>", self.on_drag_start)
        self.root.bind("<B1-Motion>", self.on_drag_motion)
        self.root.bind("<ButtonRelease-1>", self.on_drag_end)

        self.root.mainloop()
        
    def load_animations(self, animation_path: Optional[str] = None) -> None:
        # Load animations from folder
        if animation_path is None:
            self.animation_path = os.path.join(os.path.dirname(__file__), "animations")  # TODO: get another system path
        else:
            self.animation_path = animation_path
        self.animations = AnimationLoader.LoadAnimations(self.animation_path)
        
        # Check if animations is not None
        if self.animations is None:
            raise ValueError("Failed to load animations")
        standard_animation = self.animations.get(self.mood)
        if standard_animation is None:
            raise ValueError(f"Failed to load '{self.mood}' animation")
        if not isinstance(standard_animation, list) or len(standard_animation) == 0:
            raise ValueError(f"'{self.mood}' animation must be a non-empty list")
        if not isinstance(standard_animation[0], tk.PhotoImage):
            raise ValueError(f"First frame of '{self.mood}' animation is not a tk.PhotoImage")
        self.current_animation = standard_animation
        self.current_frame = 0

        # Get the window size
        self.width = standard_animation[0].width()
        self.height = standard_animation[0].height()

    def setup_gui(self, x: Optional[int] = None, y: Optional[int] = None, fps: int = 24) -> None:
        # Remove title bar & make it always on top
        self.root.title("KOI")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        # Set the window background to black and make it transparent
        self.root.configure(bg='black')
        self.root.wm_attributes("-transparentcolor", "black")

        # Create the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        if x is None:
            x = screen_width - self.width - 50
        if y is None:
            y = screen_height - self.height - 100
        self.x, self.y = x, y
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

        # Display the frame
        self.fps = fps
        self.delay_frame = 1000 // fps
        self.delay_animation = int(1000 * 0.5)
        self.label = tk.Label(self.root, image=self.current_animation[0], bg='black')
        self.label.pack()
        self.root.after(self.delay_animation, self.animate)

    def on_drag_start(self, event):
        """Store the initial mouse position when dragging starts."""
        self.start_x = event.x
        self.start_y = event.y

    def on_drag_motion(self, event):
        """Update the window position based on mouse movement."""
        # Directly calculate the new window position using screen coordinates
        self.root.geometry(f"+{event.x_root - self.start_x}+{event.y_root - self.start_y}")

    def on_drag_end(self, event):
        """Play animation after dragging ends."""
        self.root.after(self.delay_animation, self.animate)

    def animate(self):
        """Animate for one cycle"""
        if not self.current_animation:
            return

        self.label.config(image=self.current_animation[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.current_animation)

        if self.current_frame != 0:  # Continue until the end of the cycle
            self.root.after(self.delay_frame, self.animate)
        else:
            self.label.config(image=self.current_animation[0])  # Reset to first frame
