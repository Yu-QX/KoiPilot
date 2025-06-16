import os  # Importing the os module to interact with the file system

class FileManager:
    """
    A class to manage file operations such as renaming, moving, and removing files.
    """

    @staticmethod
    def rename_file(old_name, new_name):
        """
        Renames a file from old_name to new_name.

        :param old_name: The current name of the file.
        :param new_name: The new name for the file.
        :raises FileNotFoundError: If the file does not exist.
        :raises FileExistsError: If a file with the new name already exists.
        """
        if not os.path.exists(old_name):
            raise FileNotFoundError(f"The file '{old_name}' does not exist.")
        if os.path.exists(new_name):
            raise FileExistsError(f"A file with the name '{new_name}' already exists.")
        os.rename(old_name, new_name)

    @staticmethod
    def move_file(file_path, destination_folder):
        """
        Moves a file to a new folder.

        :param file_path: The path of the file to move.
        :param destination_folder: The folder where the file should be moved.
        :raises FileNotFoundError: If the file or destination folder does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        if not os.path.isdir(destination_folder):
            raise FileNotFoundError(f"The destination folder '{destination_folder}' does not exist.")
        new_path = os.path.join(destination_folder, os.path.basename(file_path))
        os.rename(file_path, new_path)

    @staticmethod
    def remove_file(file_path):
        """
        Removes a file.

        :param file_path: The path of the file to remove.
        :raises FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        os.remove(file_path)