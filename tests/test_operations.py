import os
import sys
import pytest

# Add the 'src' directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from FileManager.file_manager import FileManager


# Add the src directory to the Python path so we can import FileManager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Helper function that uses FileManager's methods
def rename_and_move_file(old_file_path, new_file_name, destination_folder):
    try:
        # First rename the file
        new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
        FileManager.rename_file(old_file_path, new_file_path)

        # Then move the file
        FileManager.move_file(new_file_path, destination_folder)

        # Construct the final path
        moved_file_path = os.path.join(destination_folder, new_file_name)

        # Finally remove the file
        FileManager.remove_file(moved_file_path)

        print("Operation completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Test function using pytest
def test_rename_and_move_file(tmp_path):
    # Create a temporary file for testing
    original_file = tmp_path / "example.txt"
    original_file.write_text("This is a test file.")
    print("Temporary file 'example.txt' created for testing.")

    # Define the new file name and destination folder
    new_file_name = "renamed_example.txt"
    destination_folder = tmp_path / "destination"
    destination_folder.mkdir()
    print("Destination folder created.")

    # Run the file operations using FileManager
    rename_and_move_file(str(original_file), new_file_name, str(destination_folder))

    # Check if the renamed file exists in the destination folder (should have been deleted)
    renamed_file_path = destination_folder / new_file_name
    assert not os.path.exists(original_file), "Original file should be deleted."
    assert not os.path.exists(renamed_file_path), "Renamed file should be deleted."
    print("Test completed successfully.")
