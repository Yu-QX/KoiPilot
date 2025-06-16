import os
import sys
import pytest
import logging

# Add the 'src' directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from FileManager.FileOperations import FileOperator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function that uses FileManager's methods
def rename_and_move_file(old_file_path, new_file_name, destination_folder):
    try:
        # First rename the file
        new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
        FileOperator.RenameFile(old_file_path, new_file_path)
        logger.info(f"File renamed from {old_file_path} to {new_file_path}")

        # Then move the file
        FileOperator.MoveFile(new_file_path, destination_folder)
        moved_file_path = os.path.join(destination_folder, new_file_name)
        logger.info(f"File moved to {moved_file_path}")

        # Finally remove the file
        FileOperator.RemoveFile(moved_file_path)
        logger.info(f"File removed from {moved_file_path}")

        return True

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False

# Test function using pytest
def test_rename_and_move_file(tmp_path):
    # Create a temporary file for testing
    original_file = tmp_path / "example.txt"
    original_file.write_text("This is a test file.")
    logger.info(f"Temporary file '{original_file}' created for testing.")

    # Define the new file name and destination folder
    new_file_name = "renamed_example.txt"
    destination_folder = tmp_path / "destination"
    FileOperator.CreateFolder(str(destination_folder))
    logger.info(f"Destination folder '{destination_folder}' created.")

    # Run the file operations using FileManager
    result = rename_and_move_file(str(original_file), new_file_name, str(destination_folder))
    assert result, "File operations should succeed"

    # Check if the renamed file exists in the destination folder (should have been deleted)
    renamed_file_path = destination_folder / new_file_name
    assert not os.path.exists(original_file), "Original file should be deleted."
    assert not os.path.exists(renamed_file_path), "Renamed file should be deleted."
    logger.info("Test completed successfully.")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])