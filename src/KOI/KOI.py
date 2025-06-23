import os
from typing import Optional
import tkinter as tk
from .AnimationLoader import AnimationLoader
from .Menu import KOIMenu

# Developer Note: 
# - `CamelCase` for variables and functions to export and `snake_case` for internal use 

class DesktopKOI:
    """The main class for the KOI"""
    def __init__(self, root):
        self.root = root

        # Define KOI variables (only a display for what will be used)
        self.x, self.y = 0, 0
        self.height, self.width = 0, 0
        self.animation_level = 0
        self.mood = ""

        # Launch window
        self.load_animations()  # TODO: allow config for animations
        self.setup_gui()        # TODO: remember the location when last used

        # Bind events for menu
        self.menu = KOIMenu(self.root)
        self.root.bind("<Enter>", self.menu.Show)

        # Bind events for dragging
        self.root.on_drag = False
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
        
        # Check if animations is dict
        if not isinstance(self.animations, dict):
            raise ValueError("Failed to load animations")
        self.SetMood()

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
        self.x, self.y = int(x), int(y)  # type: ignore
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

        # Display the frame
        self.fps = fps
        self.delay_frame = 1000 // fps
        self.delay_animation = int(1000 * 0.5)
        self.label = tk.Label(self.root, image=self.current_animation[0], bg='black')
        self.label.pack()
        self.root.after(self.delay_animation, self.Animate)

        # DEBUG
        # TODO: remove this after debug
        # self.rootdebug = tk.Tk()
        # self.rootdebug.title("DEBUG")
        # self.rootdebug.overrideredirect(True)
        # self.rootdebug.attributes('-topmost', True)
        # self.rootdebug.geometry(f"{screen_width}x{screen_height}+0+0")
        # self.rootdebug.configure(bg='black')
        # self.rootdebug.wm_attributes("-transparentcolor", "black")
        # self.canvas = tk.Canvas(self.rootdebug, bg='black', highlightthickness=0, width=screen_width, height=screen_height)
        # self.canvas.place(x=0, y=0)

    def on_drag_start(self, event):
        """Store the initial mouse position when dragging starts."""
        self.root.on_drag = True
        self.start_x = event.x
        self.start_y = event.y
        self.animation_level = 10
        self.menu.Hide()

        # DEBUG
        # self.clear_boundary()

    def on_drag_motion(self, event):
        """Update the window position based on mouse movement."""
        # Directly calculate the new window position using screen coordinates
        self.root.geometry(f"+{event.x_root - self.start_x}+{event.y_root - self.start_y}")

    def on_drag_end(self, event):
        """Play animation after dragging ends."""
        self.root.after(self.delay_animation, self.Animate)
        # get the current window position
        self.x, self.y = self.root.winfo_x(), self.root.winfo_y()
        self.animation_level = 0
        self.root.on_drag = False

        # DEBUG
        # self.draw_boundary(self.x, self.y, self.x + self.width, self.y + self.height)

    def SetMood(self, mood: str = "standard"):
        """Change the mood of KOI"""
        self.mood = mood
        preparatory_animation = self.animations.get(self.mood)
        if preparatory_animation is None:
            raise ValueError(f"Failed to load '{self.mood}' animation")
        if not isinstance(preparatory_animation, list) or len(preparatory_animation) == 0:
            raise ValueError(f"'{self.mood}' animation must be a non-empty list")
        if not isinstance(preparatory_animation[0], tk.PhotoImage):
            raise ValueError(f"First frame of '{self.mood}' animation is not a tk.PhotoImage")
        self.current_animation = preparatory_animation
        self.current_frame = 0

        # Get the window size
        self.width = preparatory_animation[0].width()
        self.height = preparatory_animation[0].height()
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

    def Animate(self, animation_level: int = 0, reset_mood: bool = True):
        """Animate for one cycle"""
        if not self.current_animation:
            return

        self.label.config(image=self.current_animation[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.current_animation)

        if self.current_frame != 0 and self.animation_level <= animation_level:  # Continue until the end of the cycle or a higher level take over
            self.root.after(self.delay_frame, self.Animate, (animation_level))
        else:
            self.current_frame = 0
            self.label.config(image=self.current_animation[self.current_frame])  # Reset to first frame
            if reset_mood:
                self.SetMood()

    # DEBUG
    # def clear_boundary(self):
    #     """Clear previously drawn boundary rectangles."""
    #     self.canvas.delete("boundary")

    # DEBUG
    # def draw_boundary(self, x1, y1, x2, y2, color="#FF0000"):
    #     """Draw a rectangle around the animation window."""
    #     self.canvas.create_rectangle(
    #         x1, y1, x2, y2,
    #        outline=color, dash=(4, 4), tags="boundary"
    #     )
    #     print(f"{x1}\t{x2}\t{y1}\t{y2}")