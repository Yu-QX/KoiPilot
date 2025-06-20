import sys, os
from FileManager.Counsellor import Counsellor
from FileManager.Operations import FileOperator, FolderOperator
from Listeners import Listener

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

