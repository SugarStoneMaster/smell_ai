import subprocess
import os
import csv
from datetime import datetime

count_report_path = "../../general_output/count_report.py"
test_folder = "./test_cases/"
files_to_clean = ["project_overview.csv", "general_overview.csv"]
output_folder = "./incident_reports/"


test_cases = [
    # TC_2.1: Correct overview_output.csv
    {"id": "TC_2.1", "csv_file": "overview_output_valid.csv", "expected": "Ausiliary charts generated"},

    # TC_2.2: Columns with wrong data types
    {"id": "TC_2.2", "csv_file": "overview_output_invalid_columns.csv", "expected": "Error: Columns datatypes not correct"},

    # TC_2.3: Missing required columns
    {"id": "TC_2.3", "csv_file": "overview_output_missing_columns.csv", "expected": "Error: CSV file must contain 'filename', 'name_smell' and 'smell' columns."},

    # TC_2.4: Empty file
    {"id": "TC_2.4", "csv_file": "overview_output_empty.csv", "expected": "Error: The input CSV file is empty."},

    # TC_2.5: Invalid file format (non-csv)
    {"id": "TC_2.5", "csv_file": "overview_output_invalid_format.png", "expected": "Error: The input file is not a valid CSV format."},

    # TC_2.6: File does not exist
    {"id": "TC_2.6", "csv_file": "non_existent_file.csv", "expected": "Error: File './test_cases/non_existent_file.csv' not found."}
]

def clean_output_files():
    """
    Remove the output files if they exist.
    """
    for file_name in files_to_clean:
        file_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed {file_name}")
        else:
            print(f"{file_name} not found, no need to remove")


def run_test_case(test_case, writer):
    csv_file = os.path.join(test_folder, test_case["csv_file"])

    if not os.path.exists(csv_file) and test_case["id"] != "TC_2.6":
        message = f"File {test_case['csv_file']} not found."
        writer.writerow([datetime.now(), test_case["id"], "Failed", message])
        print(f"Test case {test_case['id']} failed: {message}")
        return

    try:
        command = ['python3', count_report_path, '--input', csv_file]

        result = subprocess.run(command, capture_output=True, text=True)

        if test_case["expected"] in result.stdout:
            writer.writerow([datetime.now(), test_case["id"], "Passed", ""])
            print(f"Test case {test_case['id']} passed.")
        else:
            message = f"Expected: {test_case['expected']}. Got: {result.stdout.strip()}"
            writer.writerow([datetime.now(), test_case["id"], "Failed", message])
            print(f"\033[91mTest case {test_case['id']} failed. {message}\033[0m")

    except Exception as e:
        message = f"Error running test case {test_case['id']}: {e}"
        writer.writerow([datetime.now(), test_case["id"], "Failed", message])
        print(f"Error running test case {test_case['id']}: {e}")

def main():
    clean_output_files()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    execution_count = len(os.listdir(output_folder)) + 1
    incident_report_path = os.path.join(output_folder, f"incident_report_execution_{execution_count}.csv")

    with open(incident_report_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Test Case ID", "Outcome", "Message"])

        for test_case in test_cases:
            run_test_case(test_case, writer)


if __name__ == '__main__':
    main()