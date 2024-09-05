import argparse
import sys

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def temporal_chart(input_file):
    """
    Given a .csv file with smells and date columns, creates a temporal chart which
    highlights the number of smells between different dates/executions.
    """

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Error: The input CSV file is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        print("Error: The input file is not a valid CSV format.")
        sys.exit(1)

    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Sort DataFrame by date
    df = df.sort_values('date')

    # Reset index to use in plot
    df.reset_index(drop=True, inplace=True)

    # Start the plot
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot using the index for x-axis and smells for y-axis
    ax1.plot(df.index + 1, df['smells'], marker='o', linestyle='-')  # adding 1 to start index from 1
    ax1.set_title('Number of Smells Over Time')
    ax1.set_xlabel('Execution Index')
    ax1.set_ylabel('Number of Smells')
    ax1.grid(True)

    # Create secondary x-axis to show dates
    ax2 = ax1.twiny()
    ax2.set_xlabel('Date')

    # Set x-ticks on secondary axis to match the primary axis
    ax2.set_xlim(ax1.get_xlim())  # Ensure the x-limits are the same
    ax2.set_xticks(ax1.get_xticks())  # Use the same x-ticks as ax1
    # Convert index positions to dates and set them as labels on the secondary axis
    tick_labels = [df['date'].iloc[int(tick) - 1].strftime('%Y-%m-%d') if tick <= len(df['date']) else '' for tick in
                   ax1.get_xticks()]
    ax2.set_xticklabels(tick_labels)

    # Ensure y-axis has integer labels
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Show plot
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Generate a temporal chart of smells over time")
    parser.add_argument('--input', type=str, required=True, help="Path to the input .csv file")

    args = parser.parse_args()

    temporal_chart(args.input)

    print("Temporal chart generated")
    sys.exit(0)


if __name__ == "__main__":
    main()