import argparse
import pandas as pd
import matplotlib.pyplot as plt
import sys


def label_threshold(pct, all_labels, threshold=10):
    """
    Only display the label if the percentage is greater than the threshold.
    """
    return all_labels if pct > threshold else ''


def pie_or_bar_chart(input_file="./general_overview.csv", is_pie=False):
    """
    Generate a pie or bar chart in which the frequencies for type of code smell are shown.
    input_file should be a .csv with "name_smell" and "smell" columns, which are respectively
    type of code smell and frequency.
    """
    try:
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Error: The input CSV file is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        print("Error: The input file is not a valid CSV format.")
        sys.exit(1)
    #except Exception:
       # print("Error: The input file is not a valid CSV format.")
       # sys.exit(1)

    # Ensure the file has the correct columns
    if 'name_smell' not in data.columns or 'smell' not in data.columns:
        print("Error: CSV file must contain 'name_smell' and 'smell' columns.")
        sys.exit(1)

    code_smells = data['name_smell']
    frequencies = data['smell']
    if is_pie:
        # Calculate percentage for each code smell
        total = sum(frequencies)
        percentages = [(freq / total) * 100 for freq in frequencies]

        plt.figure(figsize=(14, 8))

        # Custom labels based on threshold
        labels = [label_threshold(pct, label, threshold=10) for pct, label in zip(percentages, code_smells)]

        wedges, texts, autotexts = plt.pie(
            frequencies, labels=labels, autopct='%1.1f%%', startangle=140,
            textprops={'fontsize': 10}, pctdistance=0.85)

        for autotext in autotexts:
            autotext.set_size(10)

        plt.title('Percentage of Code Smells', fontsize=16)
        plt.axis('equal')

        plt.legend(code_smells, title="Code Smells", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        plt.tight_layout()
        plt.show()
        print("Pie chart generated")
        sys.exit(0)
    else:
        # Bar chart
        plt.figure(figsize=(14, 8))
        plt.bar(code_smells, frequencies, color='purple')
        plt.xlabel('Code Smell')
        plt.ylabel('Frequency')
        plt.title('Number of Code Smells by Type')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        print("Bar chart generated")
        sys.exit(0)
def main():
    parser = argparse.ArgumentParser(
        description="Generate a chart (pie or bar) based on code smell data in a CSV file.")
    parser.add_argument('--input', type=str, default="./general_overview.csv", help='Path to the input CSV file.')
    parser.add_argument('--pie', action='store_true', help='Flag to generate a pie chart. Generates a bar chart if omitted.')

    args = parser.parse_args()

    pie_or_bar_chart(input_file=args.input, is_pie=args.pie)


if __name__ == '__main__':
    main()
