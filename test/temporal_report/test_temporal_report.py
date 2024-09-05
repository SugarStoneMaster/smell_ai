import subprocess
import os
import csv
from datetime import datetime

temporal_report_path = "../../general_output/temporal_report.py"
test_folder = "./test_cases/"
output_folder = "./incident_reports/"

test_cases = [
    # TC_4.1: Correct smell_count_dates.csv
    {"id": "TC_4.1", "csv_file": "smell_count_dates_valid.csv", "expected": "Temporal chart generated"},

    # TC_4.2: Columns with wrong data types
    {"id": "TC_4.2", "csv_file": "smell_count_dates_invalid_columns.csv", "expected": "Error: Columns datatype not correct"},

    # TC_4.3: Missing required columns
    {"id": "TC_4.3", "csv_file": "smell_count_dates_missing_columns.csv", "expected": "Error: CSV file must contain 'smells' and 'date' columns."},

    # TC_4.4: Empty file
    {"id": "TC_4.4", "csv_file": "smell_count_dates_empty.csv", "expected": "Error: The input CSV file is empty."},

    # TC_4.5: Invalid file format (non-csv)
    {"id": "TC_4.5", "csv_file": "smell_count_dates_invalid_format.png", "expected": "Error: The input file is not a valid CSV format."},

    # TC_4.6: File does not exist
    {"id": "TC_4.6", "csv_file": "non_existent_file.csv", "expected": "Error: File './test_cases/non_existent_file.csv' not found."}
]


def run_test_case(test_case, writer):
    csv_file = os.path.join(test_folder, test_case["csv_file"])

    if not os.path.exists(csv_file) and test_case["id"] != "TC_4.6":
        message = f"File {test_case['csv_file']} not found."
        writer.writerow([datetime.now(), test_case["id"], "Failed", message])
        print(f"Test case {test_case['id']} failed: {message}")
        return

    try:
        command = ['python3', temporal_report_path, '--input', csv_file]

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

    with open(incident_report_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Test Case ID", "Outcome", "Message"])

        for test_case in test_cases:
            run_test_case(test_case, writer)


if __name__ == '__main__':
    main()