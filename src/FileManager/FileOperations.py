import os

class FileOperator:
    """
    The `FileOperator` class provides methods for operating with files & folders.
    It also contains security checks to prevent unauthorized access. # Not Yet Implemented
    """

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