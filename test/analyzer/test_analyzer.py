import argparse
import subprocess
import os
import csv
from datetime import datetime

analyzer_path = "../../controller/analyzer.py"
test_folder = "./test_cases/"
output_folder = "./test/analyzer/incident_reports/"

# Test case paths and expected outcomes
test_cases = [
    # Test Case 1: Non contiene files python
    {"id": "TC_1",
     "args": ["--input", "../test/analyzer/test_cases/no_python_files/input", "--output", "../test/analyzer/test_cases/no_python_files/output", "--multiple", "--parallel"],
     "expected": "Error: No Python files found."},

    # Test Case 2: Il path non esiste
    {"id": "TC_2",
     "args": ["--input", "../test/analyzer/test_cases/non_existent_path/input", "--output", "../test/analyzer/test_cases/non_existent_path/output"],
     "expected": "Error: Input path does not exist."},

    # Test Case 3: Contiene solo files di test python
    {"id": "TC_3",
     "args": ["--input", "../test/analyzer/test_cases/test_files_only/input", "--output", "../test/analyzer/test_cases/test_files_only/output"],
     "expected": "Error: No valid Python files found."},

    # Test Case 4: Il path esiste ma non ci sono files
    {"id": "TC_4",
     "args": ["--input", "../test/analyzer/test_cases/empty_folder/input", "--output", "../test/analyzer/test_cases/empty_folder/output"],
     "expected": "Error: No files found in the input folder."},

    # Test Case 5: Il path non è una cartella
    {"id": "TC_5",
     "args": ["--input", "../test/analyzer/test_cases/not_a_directory_input/input/general_overview.csv", "--output", "../test/analyzer/test_cases/not_a_directory_input/output"],
     "expected": "Error: The input path is not a directory."},

    # Test Case 6: Contiene una cartella esistente ma non scrivibile
    {"id": "TC_6",
     "args": ["--input", "../test/analyzer/test_cases/not_writable_folder/input", "--output", "../test/analyzer/test_cases/not_writable_folder/output"],
     "expected": "Error: Output folder is not writable."},

    # Test Case 7: Contiene una cartella non esistente
    {"id": "TC_7",
     "args": ["--input", "../test/analyzer/test_cases/not_existent_output_folder/input", "--output", "../test/analyzer/test_cases/not_existent_output_folder/output"],
     "expected": "Output folder created."},

    # Test Case 8: Il path esiste ma contiene un file
    {"id": "TC_8",
     "args": ["--input", "../test/analyzer/test_cases/not_a_directory_output/input", "--output", "../test/analyzer/test_cases/not_a_directory_output/output/general_overview.csv"],
     "expected": "Error: The input path is not a directory."},

    # Test Case 9: L'execution_log non esiste (resume set to True)
    {"id": "TC_9",
     "args": ["--input", "../test/analyzer/test_cases/no_execution_log/input", "--output", "../test/analyzer/test_cases/no_execution_log/output", "--multiple", "--resume"],
     "expected": "Error: L'execution_log non esiste."},

    # Test Case 10: Numero Threads = 0 (invalid for parallel execution)
    {"id": "TC_10",
     "args": ["--input", "../test/analyzer/test_cases/zero_threads/input", "--output", "../test/analyzer/test_cases/zero_threads/output", "--multiple", "--parallel", "--max_workers", "0"],
     "expected": "Error: Invalid number of threads for parallel execution."},

    # Test Case 11: Single project with parallel execution (valid case)
    {"id": "TC_11",
     "args": ["--input", "../test/analyzer/test_cases/single_project/input", "--output", "../test/analyzer/test_cases/single_project/output", "--multiple", "--parallel"],
     "expected": "I report del singolo progetto vengono generati in maniera parallela."},

    # Test Case 12: Single project with parallel execution (valid case with threads 1-10)
    {"id": "TC_12",
     "args": ["--input", "../test/analyzer/test_cases/single_project/input", "--output", "../test/analyzer/test_cases/single_project/output", "--multiple", "--parallel", "--max_workers", "5"],
     "expected": "I report del singolo progetto vengono generati in maniera parallela."},

    # Test Case 13: Single project with parallel execution (valid case with threads >10)
    {"id": "TC_13",
     "args": ["--input", "../test/analyzer/test_cases/single_project", "--output", "../test/analyzer/test_cases/single_project/output", "--multiple", "--parallel", "--max_workers", "15"],
     "expected": "I report del singolo progetto vengono generati in maniera parallela."},

    # Test Case 14: Single project with sequential execution and resume
    {"id": "TC_14",
     "args": ["--input", "../test/analyzer/test_cases/single_project/input", "--output", "../test/analyzer/test_cases/single_project/output", "--multiple", "--resume"],
     "expected": "I report del singolo progetto vengono generati in maniera sequenziale controllando l'execution_log."},

    # Test Case 15: Single project with sequential execution
    {"id": "TC_15",
     "args": ["--input", "../test/analyzer/test_cases/single_project/input", "--output", "../test/analyzer/test_cases/single_project/output", "--multiple"],
     "expected": "I report del singolo progetto vengono generati in maniera sequenziale."},

    # Test Case 16: Single project with no sequential execution, no resume, no parallel
    {"id": "TC_16",
     "args": ["--input", "../test/analyzer/test_cases/single_project/input", "--output", "../test/analyzer/test_cases/single_project/output"],
     "expected": "I report del singolo progetto vengono generati."},

    # Test Case 17: Single project with 11-50 Python files, parallel execution
    {"id": "TC_17",
     "args": ["--input", "../test/analyzer/test_cases/single_project_large/input", "--output", "../test/analyzer/test_cases/single_project_large/output", "--multiple", "--parallel"],
     "expected": "I report del singolo progetto vengono generati in maniera parallela."},

    # Test Case 18: Single project with 11-50 Python files, parallel execution with 1-10 threads
    {"id": "TC_18",
     "args": ["--input", "../test/analyzer/test_cases/single_project_large/input", "--output", "../test/analyzer/test_cases/single_project_large/output", "--multiple", "--parallel", "--max_workers", "5"],
     "expected": "I report del singolo progetto vengono generati in maniera parallela."},

    # Test Case 19: Single project with 11-50 Python files, parallel execution with >10 threads
    {"id": "TC_19",
     "args": ["--input", "../test/analyzer/test_cases/single_project_large/input", "--output", "../test/analyzer/test_cases/single_project_large/output", "--multiple", "--parallel", "--max_workers", "15"],
     "expected": "I report del singolo progetto vengono generati in maniera parallela."},

    # Test Case 20: Single project with 11-50 Python files, sequential execution with resume
    {"id": "TC_20",
     "args": ["--input", "../test/analyzer/test_cases/single_project_large/input", "--output", "../test/analyzer/test_cases/single_project_large/output", "--multiple", "--resume"],
     "expected": "I report del singolo progetto vengono generati in maniera sequenziale controllando l'execution_log."},

    # Test Case 21: Single project with 11-50 Python files, sequential execution
    {"id": "TC_21",
     "args": ["--input", "../test/analyzer/test_cases/single_project_large/input", "--output", "../test/analyzer/test_cases/single_project_large/output"],
     "expected": "I report del singolo progetto vengono generati in maniera sequenziale."},

    # Test Case 22: Single project with 11-50 Python files
    {"id": "TC_22",
     "args": ["--input", "../test/analyzer/test_cases/single_project_huge/input", "--output", "../test/analyzer/test_cases/single_project_huge/output"],
     "expected": "I report del singolo progetto vengono generati."},

    # Test Case 24: Single project with 51+ Python files, parallel execution with 1-10 threads
    {"id": "TC_24",
     "args": ["--input", "../test/analyzer/test_cases/single_project_huge/input", "--output", "../test/analyzer/test_cases/single_project_huge/output", "--multiple", "--parallel", "--max_workers", "8"],
     "expected": "I report del singolo progetto vengono generati in maniera parallela."},

    # Test Case 25: Single project with 51+ Python files, parallel execution with >10 threads
    {"id": "TC_25",
     "args": ["--input", "../test/analyzer/test_cases/single_project_huge/input", "--output", "../test/analyzer/test_cases/single_project_huge/output", "--multiple", "--parallel", "--max_workers", "12"],
     "expected": "I report del singolo progetto vengono generati in maniera parallela."},

    # Test Case 26: Single project with 51+ Python files, sequential execution with resume
    {"id": "TC_26",
     "args": ["--input", "../test/analyzer/test_cases/single_project_huge/input", "--output", "../test/analyzer/test_cases/single_project_huge/output", "--multiple", "--resume"],
     "expected": "I report del singolo progetto vengono generati in maniera sequenziale controllando l'execution_log."},

    # Test Case 27: Single project with 51+ Python files, sequential execution
    {"id": "TC_27",
     "args": ["--input", "../test/analyzer/test_cases/single_project_huge/input", "--output", "../test/analyzer/test_cases/single_project_huge/output", "--multiple"],
     "expected": "I report del singolo progetto vengono generati in maniera sequenziale."},

    # Test Case 28: Single project with 51+ Python files
    {"id": "TC_28",
     "args": ["--input", "../test/analyzer/test_cases/single_project_huge/input", "--output", "../test/analyzer/test_cases/single_project_huge/output"],
     "expected": "I report del singolo progetto vengono generati."},

    # Test Case 29: Multiple projects (2 <= N <= 10), parallel execution
    {"id": "TC_29",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_small/input", "--output", "../test/analyzer/test_cases/multiple_projects_small/output", "--multiple", "--parallel"],
     "expected": "I report dei progetti vengono generati in maniera parallela."},

    # Test Case 30: Multiple projects (2 <= N <= 10), parallel execution with 1-10 threads
    {"id": "TC_30",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_small/input", "--output", "../test/analyzer/test_cases/multiple_projects_small/output", "--multiple", "--parallel", "--max_workers", "5"],
     "expected": "I report dei progetti vengono generati in maniera parallela."},

    # Test Case 31: Multiple projects (2 <= N <= 10), parallel execution with >10 threads
    {"id": "TC_31",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_small/input", "--output", "../test/analyzer/test_cases/multiple_projects_small/output", "--multiple", "--parallel", "--max_workers", "12"],
     "expected": "I report dei progetti vengono generati in maniera parallela."},

    # Test Case 32: Multiple projects (2 <= N <= 10), sequential execution with resume
    {"id": "TC_32",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_small/input", "--output", "../test/analyzer/test_cases/multiple_projects_small/output", "--multiple", "--resume"],
     "expected": "I report dei progetti vengono generati in maniera sequenziale controllando l'execution_log."},

    # Test Case 33: Multiple projects (2 <= N <= 10), sequential execution
    {"id": "TC_33",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_small/input", "--output", "../test/analyzer/test_cases/multiple_projects_small/output", "--multiple"],
     "expected": "I report dei progetti vengono generati in maniera sequenziale."},

    # Test Case 34: Multiple projects (N >= 11), parallel execution
    {"id": "TC_34",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_large/input", "--output", "../test/analyzer/test_cases/multiple_projects_large/output"],
     "expected": "I report dei progetti vengono generati e aggregati tra loro."},

    # Test Case 35: Multiple projects (N >= 11), parallel execution
    {"id": "TC_35",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_large/input", "--output", "../test/analyzer/test_cases/multiple_projects_large/output", "--multiple", "--parallel"],
     "expected": "I report dei progetti vengono generati in maniera parallela."},

    # Test Case 36: Multiple projects (N >= 11), parallel execution with 1-10 threads
    {"id": "TC_36",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_large/input", "--output", "../test/analyzer/test_cases/multiple_projects_large/output", "--multiple", "--parallel", "--max_workers", "8"],
     "expected": "I report dei progetti vengono generati in maniera parallela."},

    # Test Case 37: Multiple projects (N >= 11), parallel execution with >10 threads
    {"id": "TC_37",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_large/input", "--output", "../test/analyzer/test_cases/multiple_projects_large/output", "--multiple", "--parallel", "--max_workers", "12"],
     "expected": "I report dei progetti vengono generati in maniera parallela."},

    # Test Case 38: Multiple projects (N >= 11), sequential execution with resume
    {"id": "TC_38",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_large/input", "--output", "../test/analyzer/test_cases/multiple_projects_large/output", "--multiple", "--resume"],
     "expected": "I report dei progetti vengono generati in maniera sequenziale controllando l'execution_log."},

    # Test Case 39: Multiple projects (N >= 11), sequential execution
    {"id": "TC_39",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_large/input", "--output", "../test/analyzer/test_cases/multiple_projects_large/output", "multiple"],
     "expected": "I report dei progetti vengono generati in maniera sequenziale."},

    # Test Case 40: Multiple projects (N >= 11), sequential execution
    {"id": "TC_40",
     "args": ["--input", "../test/analyzer/test_cases/multiple_projects_large/input", "--output", "../test/analyzer/test_cases/multiple_projects_large/output"],
     "expected": "I report dei progetti vengono e aggreati tra loro."},

]


def run_test_case(test_case, writer):
    try:
        command = ['python3', analyzer_path] + test_case['args']

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
    parser = argparse.ArgumentParser(description="Run test cases sequentially or one by one.")
    parser.add_argument('--mode', type=str, choices=['sequential', 'step'], default='sequential',
                        help="Execution mode: 'sequential' runs all test cases without stopping, 'step' stops after each test case.")
    args = parser.parse_args()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    execution_count = len(os.listdir(output_folder)) + 1
    incident_report_path = os.path.join(output_folder, f"incident_report_execution_{execution_count}.csv")

    with open(incident_report_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Test Case ID", "Outcome", "Message"])

        for test_case in test_cases:
            run_test_case(test_case, writer)

            if args.mode == 'step':
                input(f"Press Enter to continue to the next test case...")

    print(f"Execution completed. Incident report saved at: {incident_report_path}")


if __name__ == '__main__':
    main()