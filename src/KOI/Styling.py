from dataclasses import dataclass

@dataclass
class Styling:
    """Collection of style parameters"""
    # Colors
    color_background = "#333333"
    color_outline = "#444444"
    color_text = "#FFFFFF"
    color_pointed = "#666666"

    # Times (ms)
    duration_fade = 200  # The duration of the fade in ms

    # Shapes
    shape_corner_radius = 15

    # Fonts
    font_family = "Courier"
    font_size = 12