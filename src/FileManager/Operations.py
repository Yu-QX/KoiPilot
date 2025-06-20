import os
import shutil

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
        if not os.path.exists(old_name):
            return 210111  # Source File Not Found
        if os.path.exists(new_name):
            return 210115  # Destination File Already Exists
        os.rename(old_name, new_name)
        return 210000  # Success

    @staticmethod
    def MoveFile(file_path: str, destination_folder: str) -> int:
        """
        Moves a file to a new folder.

        :param file_path: The path of the file to move.
        :param destination_folder: The folder where the file should be moved.
        :return: An error code indicating the result of the operation.
        """
        if not os.path.exists(file_path):
            return 210111  # Source File Not Found
        if not os.path.isdir(destination_folder):
            return 210114  # Destination Folder Not Found
        new_path = os.path.join(destination_folder, os.path.basename(file_path))
        os.rename(file_path, new_path)
        return 210000  # Success

    @staticmethod
    def RemoveFile(file_path: str) -> int:
        """
        Removes a file.

        :param file_path: The path of the file to remove.
        :return: An error code indicating the result of the operation.
        """
        if not os.path.exists(file_path):
            return 210111  # Source File Not Found
        os.remove(file_path)
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
        if os.path.exists(folder_path) and not exist_ok:
            return 210113  # Folder Already Exists
        os.makedirs(folder_path, exist_ok=exist_ok)
        return 210000  # Success

    @staticmethod
    def RenameFolder(old_name: str, new_name: str) -> int:
        """
        Renames a folder from old_name to new_name.

        :param old_name: The current name of the folder.
        :param new_name: The new name for the folder.
        :return: An error code indicating the result of the operation.
        """
        if not os.path.exists(old_name):
            return 210114  # Destination Folder Not Found
        if os.path.exists(new_name):
            return 210113  # Folder Already Exists
        os.rename(old_name, new_name)
        return 210000  # Success

    @staticmethod
    def RemoveFolder(folder_path: str) -> int:
        """
        Removes a folder, including all sub-folders and files.

        :param folder_path: The path of the folder to remove.
        :return: An error code indicating the result of the operation.
        """
        if not os.path.exists(folder_path):
            return 210114  # Destination Folder Not Found
        shutil.rmtree(folder_path)
        if not os.path.exists(folder_path):  # Check if the folder was successfully removed
            return 210122  # Folder Operation Error
        return 210000  # Success

    @staticmethod
    def MoveFolder(folder_path: str, destination_folder: str) -> int:
        """
        Moves a folder to a new location.

        :param folder_path: The path of the folder to move.
        :param destination_folder: The folder where the folder should be moved.
        :return: An error code indicating the result of the operation.
        """
        if not os.path.exists(folder_path):
            return 210114  # Destination Folder Not Found
        if not os.path.isdir(destination_folder):
            return 210114  # Destination Folder Not Found
        new_path = os.path.join(destination_folder, os.path.basename(folder_path))
        os.rename(folder_path, new_path)
        return 210000  # Success
