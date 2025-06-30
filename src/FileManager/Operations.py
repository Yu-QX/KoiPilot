import os, sys
import shutil, json

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

from Environment import PATH_SECURITY_FILE, load_json_with_backup
from Environment import Logger

class Guard:
    """Prevent illegal operations"""
    def __init__(self, security_file: str = PATH_SECURITY_FILE):
        self.path = security_file
        self.mode_list = ("R", "W", "D")
        self.logger = Logger("File Guard")
        self.Load()

    def Load(self) -> dict:
        """
        Load security file

        :return: Security file
        """
        self.security_info = load_json_with_backup(self.path, {}, "security")
        return self.security_info

    def Save(self):
        """
        Save security file
        """
        with open(self.path, 'w') as f:
            json.dump(self.security_info, f, indent=2)

    def Add(self, path: str, mode: str):
        """
        Add a path to security file

        :param path: Path to add
        :param mode: Mode to add
        """
        success = False
        mode = mode.upper()
        # Format path
        path = os.path.abspath(path)

        # Add path if not exists
        if mode in self.mode_list:
            if path not in self.security_info.get(mode, []):
                self.security_info.setdefault(mode, []).append(path)
                success = True
        
        # Save
        if success:
            self.logger.Log(f"+{mode} {path}")
        self.Save()
        return success

    def Remove(self, path: str, mode: str):
        """
        Remove a path from security file

        :param path: Path to remove
        :param mode: Mode to remove
        """
        success = False
        mode = mode.upper()
        # Format path
        path = os.path.abspath(path)

        # Remove path if exists
        if mode in self.mode_list and path in self.security_info.get(mode, []):
            self.security_info[mode].remove(path)
            success = True
        
        # Save
        if success:
            self.logger.Log(f"-{mode} {path}")
        self.Save()
        return success

    def Check(self, path: str, mode: str) -> bool:
        """
        Check if a path is allowed

        :param path: Path to check
        :param mode: Mode to check
        :return: True if allowed, False otherwise
        """
        mode = mode.upper()
        # Format path
        path = os.path.abspath(path)

        # Check path
        result = mode in self.mode_list and path in self.security_info.get(mode, [])

        # Log
        self.logger.Log(f"{path} -> {mode}: {result}")
        return result


class FileOperator:
    """Methods for operating with files."""
    @staticmethod
    def RenameFile(old_name: str, new_name: str) -> int:
        """
        Renames a file from old_name to new_name.

        :param old_name: The current name of the file.
        :param new_name: The new name for the file.
        :return: An error code indicating the result of the operation.
        """
        # Check permissions: D+W in parent folder
        source_parent = os.path.dirname(old_name)
        dest_parent = os.path.dirname(new_name)
        if not Guard().Check(source_parent, "D"):
            return 210103  # Delete Permission Denied (source)
        if not Guard().Check(dest_parent, "W"):
            return 210102  # Write Permission Denied (destination)

        if not os.path.exists(old_name):
            return 210111  # Source File Not Found
        if os.path.exists(new_name):
            return 210115  # Destination File Already Exists
        os.rename(old_name, new_name)
        Logger("File Operator").Log(f"RenameFile: {old_name} -> {new_name}")
        return 210000  # Success

    @staticmethod
    def MoveFile(file_path: str, destination_folder: str) -> int:
        """
        Moves a file to a new folder.

        :param file_path: The path of the file to move.
        :param destination_folder: The folder where the file should be moved.
        :return: An error code indicating the result of the operation.
        """
        # Check permissions: D in source; W in destination
        source_parent = os.path.dirname(file_path)
        if not Guard().Check(source_parent, "D"):
            return 210103  # Delete Permission Denied (source)
        if not Guard().Check(destination_folder, "W"):
            return 210102  # Write Permission Denied (destination)

        if not os.path.exists(file_path):
            return 210111  # Source File Not Found
        if not os.path.isdir(destination_folder):
            return 210114  # Destination Folder Not Found
        new_path = os.path.join(destination_folder, os.path.basename(file_path))
        os.rename(file_path, new_path)
        Logger("File Operator").Log(f"MoveFile: {file_path} -> {new_path}")
        return 210000  # Success

    @staticmethod
    def RemoveFile(file_path: str) -> int:
        """
        Removes a file.

        :param file_path: The path of the file to remove.
        :return: An error code indicating the result of the operation.
        """
        # Check permissions: D in parent folder
        parent_folder = os.path.dirname(file_path)
        if not Guard().Check(parent_folder, "D"):
            return 210103  # Delete Permission Denied

        if not os.path.exists(file_path):
            return 210111  # Source File Not Found
        os.remove(file_path)
        Logger("File Operator").Log(f"RemoveFile: {file_path} -> Removed")
        return 210000  # Success

class FolderOperator:
    """Methods for operating with folders."""
    @staticmethod
    def CreateFolder(folder_path: str, exist_ok: bool = False) -> int:
        """
        Creates a new folder.

        :param folder_path: The path of the folder to create.
        :param exist_ok: If True, an existing folder will not cause an error.
        :return: An error code indicating the result of the operation.
        """
        # Check permissions: W in parent folder
        parent_folder = os.path.dirname(folder_path)
        if not Guard().Check(parent_folder, "W"):
            return 210102  # Write Permission Denied

        if os.path.exists(folder_path) and not exist_ok:
            return 210113  # Folder Already Exists
        os.makedirs(folder_path, exist_ok=exist_ok)
        Logger("Folder Operator").Log(f"CreateFolder: {folder_path} -> Created")
        return 210000  # Success

    @staticmethod
    def RenameFolder(old_name: str, new_name: str) -> int:
        """
        Renames a folder from old_name to new_name.

        :param old_name: The current name of the folder.
        :param new_name: The new name for the folder.
        :return: An error code indicating the result of the operation.
        """
        # Check permissions: D+W in parent folder
        old_parent = os.path.dirname(old_name)
        new_parent = os.path.dirname(new_name)
        if not Guard().Check(old_parent, "D"):
            return 210103  # Delete Permission Denied (old folder)
        if not Guard().Check(new_parent, "W"):
            return 210102  # Write Permission Denied (new folder)

        if not os.path.exists(old_name):
            return 210114  # Destination Folder Not Found
        if os.path.exists(new_name):
            return 210113  # Folder Already Exists
        os.rename(old_name, new_name)
        Logger("Folder Operator").Log(f"RenameFolder: {old_name} -> {new_name}")
        return 210000  # Success

    @staticmethod
    def RemoveFolder(folder_path: str) -> int:
        """
        Removes a folder, including all sub-folders and files.

        :param folder_path: The path of the folder to remove.
        :return: An error code indicating the result of the operation.
        """
        # Check permissions: D in parent folder
        parent_folder = os.path.dirname(folder_path)
        if not Guard().Check(parent_folder, "D"):
            return 210103  # Delete Permission Denied

        if not os.path.exists(folder_path):
            return 210114  # Destination Folder Not Found
        shutil.rmtree(folder_path)
        if not os.path.exists(folder_path):  # Check if the folder was successfully removed
            Logger("Folder Operator").Log(f"RemoveFolder: {folder_path} -> Removed")
            return 210000  # Success
        return 210122  # Folder Operation Error

    @staticmethod
    def MoveFolder(folder_path: str, destination_folder: str) -> int:
        """
        Moves a folder to a new location.

        :param folder_path: The path of the folder to move.
        :param destination_folder: The folder where the folder should be moved.
        :return: An error code indicating the result of the operation.
        """
        # Check permissions: D in source; W in destination
        source_parent = os.path.dirname(folder_path)
        if not Guard().Check(source_parent, "D"):
            return 210103  # Delete Permission Denied (source)
        if not Guard().Check(destination_folder, "W"):
            return 210102  # Write Permission Denied (destination)

        if not os.path.exists(folder_path):
            return 210114  # Destination Folder Not Found
        if not os.path.isdir(destination_folder):
            return 210114  # Destination Folder Not Found
        new_path = os.path.join(destination_folder, os.path.basename(folder_path))
        os.rename(folder_path, new_path)
        Logger("Folder Operator").Log(f"MoveFolder: {folder_path} -> {new_path}")
        return 210000  # Success

    @staticmethod
    def GetSubFolders(folder_path: str, full_path: bool = False) -> list[str]:
        """
        Get all sub folders in a folder

        :param folder_path: The path of the folder
        :param full_path: Whether to return the full path or just the folder name
        :return: A list of sub folders or an error code
        """
        # Check permissions: R in folder
        if not Guard().Check(folder_path, "R"):
            return []  # Read Permission Denied

        if not os.path.exists(folder_path):
            print("Error Code: 210114")  # Destination Folder Not Found
            return []
        if not os.path.isdir(folder_path):
            print("Error Code: 210122")  # Folder Operation Error
            return []

        if full_path:
            result = [entry.path for entry in os.scandir(folder_path) if entry.is_dir()]
        else:
            result = [entry.name for entry in os.scandir(folder_path) if entry.is_dir()]

        return result

    @staticmethod
    def GetFiles(folder_path: str, full_path: bool = False) -> list[str]:
        """
        Get all files in a folder

        :param folder_path: The path of the folder
        :param full_path: Whether to return the full path or just the file name
        :return: A list of files or an error code
        """
        # Check permissions: R in folder
        if not Guard().Check(folder_path, "R"):
            return []  # Read Permission Denied

        if not os.path.exists(folder_path):
            print("Error Code: 210114")  # Destination Folder Not Found
            return []
        if not os.path.isdir(folder_path):
            print("Error Code: 210122")  # Folder Operation Error
            return []

        if full_path:
            result = [entry.path for entry in os.scandir(folder_path) if entry.is_file()]
        else:
            result = [entry.name for entry in os.scandir(folder_path) if entry.is_file()]

        return result
