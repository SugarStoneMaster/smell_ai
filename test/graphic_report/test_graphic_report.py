import subprocess
import os
import csv
from datetime import datetime

graphic_report_path = "../../general_output/graphic_report.py"
test_folder = "./test_cases/"
output_folder = "./incident_reports/"

# Test case paths and expected outcomes
test_cases = [
    # TC_3.1: Correct general_overview.csv, flag pie=True
    {"id": "TC_3.1", "csv_file": "general_overview_valid.csv", "flag": "True", "expected": "Pie chart generated"},

    # TC_3.2: Correct general_overview.csv, flag pie=False
    {"id": "TC_3.2", "csv_file": "general_overview_valid.csv", "flag": "False", "expected": "Bar chart generated"},

    # TC_3.4: Columns with wrong data types
    {"id": "TC_3.4", "csv_file": "general_overview_invalid_columns.csv", "flag": "True",
     "expected": "Error: Columns datatypes not correct"},

    # TC_3.5: Missing required columns
    {"id": "TC_3.5", "csv_file": "general_overview_missing_columns.csv", "flag": "True",
     "expected": "Error: CSV file must contain 'name_smell' and 'smell' columns."},

    # TC_3.6: Empty file
    {"id": "TC_3.6", "csv_file": "general_overview_empty.csv", "flag": "True", "expected": "Error: The input CSV file is empty."},

    # TC_3.7: Invalid file format (non-csv)
    {"id": "TC_3.7", "csv_file": "general_overview_invalid_format.png", "flag": "True",
     "expected": "Error: The input file is not a valid CSV format."},

    # TC_3.8: File does not exist
    {"id": "TC_3.8", "csv_file": "non_existent_file.csv", "flag": "True", "expected": "Error: File './test_cases/non_existent_file.csv' not found."}
]


def run_test_case(test_case, writer):
    csv_file = os.path.join(test_folder, test_case["csv_file"])

    if not os.path.exists(csv_file) and test_case["id"] != "TC_3.8":
        message = f"File {test_case['csv_file']} not found."
        writer.writerow([datetime.now(), test_case["id"], "Failed", message])
        print(f"Test case {test_case['id']} failed: {message}")
        return

    try:
        command = ['python3', graphic_report_path, '--input', csv_file]

        # Add the '--pie' flag if the test case is for a pie chart
        if test_case["flag"].lower() == "true":
            command.append('--pie')

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
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    execution_count = len(os.listdir(output_folder)) + 1
    incident_report_path = os.path.join(output_folder, f"incident_report_execution_{execution_count}.csv")

    # Create a new file for this execution
    with open(incident_report_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(["Timestamp", "Test Case ID", "Outcome", "Message"])

        # Run each test case and log the result
        for test_case in test_cases:
            run_test_case(test_case, writer)


if __name__ == '__main__':
    main()