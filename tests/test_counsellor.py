import os
import sys

# Add the 'src' directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from FileManager.Counsellor import Counsellor

print("="*20)
test_cases = [
    {
        "file": "Quantum Mechanics.pdf",
        "folder_options": ["Documents/Physics", "Documents/History", "Pictures/Diagrams", "Pictures/Photos", "Pictures/Sculptures", "Pictures/Other"],
        "expected_result": "Documents/Physics"
    },
    {
        "file": "Van Gogh Painting.jpg",
        "folder_options": ["Pictures/Art", "Documents/Reports", "Pictures/Landscapes", "Documents/Presentations", "Documents/Other"],
        "expected_result": "Pictures/Art"
    },
    {
        "file": "Company Financial Report.xlsx",
        "folder_options": ["Documents/Finance", "Documents/Personal", "Pictures/Charts", "Music/Albums"],
        "expected_result": "Documents/Finance"
    }
]

for test_case in test_cases:
    counsellor = Counsellor(model="qwen3:latest")
    result = counsellor.MoveToFolder(test_case["file"], test_case["folder_options"])
    print(f"File: {test_case['file']}, Suggested Folder: {result}, Expected Folder: {test_case['expected_result']}")
    #assert result == test_case["expected_result"], f"Test failed for {test_case['file']}"

print("="*20)

name_list = name_list = [
    "2023-03-01_Report_v1.docx", "20221001_UserSurvey.csv",
    "20230515_Project_Report_v2.docx", "2022-10-01_User_Survey_Results.csv"
]

counsellor = Counsellor(model="qwen3:latest")
changes = counsellor.FormatName(name_list)
[print(f"{original_name} -> {changed_name}") for original_name, changed_name in changes.items()]
#assert changes == expected_changes, "Test failed for FormatName"