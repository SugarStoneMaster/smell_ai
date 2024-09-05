import subprocess
import os

graphic_report_path = "../../general_output/graphic_report.py"
test_folder = "./test_cases/"

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


def run_test_case(test_case):
    csv_file = os.path.join(test_folder, test_case["csv_file"])

    if not os.path.exists(csv_file) and test_case[
        "id"] != "TC_3.8":  # Ensure the test files exist, except for TC_3.8 (file doesn't exist case)
        print(f"Test case {test_case['id']} failed: file {test_case['csv_file']} not found.")
        return

    try:
        command = ['python3', graphic_report_path, '--input', csv_file]

        # Add the '--pie' flag if the test case is for a pie chart
        if test_case["flag"].lower() == "true":
            command.append('--pie')

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