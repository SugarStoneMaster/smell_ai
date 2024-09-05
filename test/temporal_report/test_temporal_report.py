import subprocess
import os

temporal_report_path = "../../general_output/temporal_report.py"
test_folder = "./test_cases/"

# Test case paths and expected outcomes
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


def run_test_case(test_case):
    csv_file = os.path.join(test_folder, test_case["csv_file"])

    if not os.path.exists(csv_file) and test_case[
        "id"] != "TC_4.6":  # Ensure the test files exist, except for TC_3.8 (file doesn't exist case)
        print(f"Test case {test_case['id']} failed: file {test_case['csv_file']} not found.")
        return

    try:
        command = ['python3', temporal_report_path, '--input', csv_file]

        result = subprocess.run(command, capture_output=True, text=True)

        if test_case["expected"] in result.stdout:
            print(f"Test case {test_case['id']} passed.")
        else:
            print(f"\033[91mTest case {test_case['id']} failed. Expected: {test_case['expected']}. Got: {result.stdout}\033[0m")
    except Exception as e:
        print(f"Error running test case {test_case['id']}: {e}")


def main():
    for test_case in test_cases:
        run_test_case(test_case)


if __name__ == '__main__':
    main()