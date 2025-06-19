import os
from pathlib import Path
from typing import Optional
import tkinter as tk


class AnimationLoader:
    @staticmethod
    def LoadAnimations(animation_folder: str) -> Optional[dict[str, list[tk.PhotoImage]]]:
        """
        Load all the animations from the given folder.

        :param animation_folder: The folder containing the animations.
        :return: A dictionary of animations, where the key is the animation name (without `.gif`) and the value is the animation file.
        """
        if not animation_folder or not os.path.isdir(animation_folder):
            return None

        animation_dict = {}
        folder_path = Path(animation_folder)

        for filename in os.listdir(folder_path):
            if filename.endswith(".gif"):
                file_path = folder_path / filename
                animation = AnimationLoader.LoadGifFrames(file_path)
                key = filename.removesuffix(".gif")
                animation_dict[key] = animation
        return animation_dict

    @staticmethod
    def LoadGifFrames(file_path: Path) -> list:
        """
        Load all frames from a GIF file.
        
        :param file_path: The path to the GIF file.
        :return: A list of PIL Image objects representing the frames.
        """
        frames = []
        try:
            while True:
                frame = tk.PhotoImage(file=str(file_path), format=f"gif -index {len(frames)}")
                frames.append(frame)
        except tk.TclError:
            # Expected when all frames are loaded or file is invalid
            pass
        return frames