import os, sys

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

from Listeners import Listener

class ChatManager:
    """Manages chat interactions."""
    def __init__(self, master, desktop_koi, koi_menu):
        pass