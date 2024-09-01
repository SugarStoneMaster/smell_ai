import argparse
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator



def temporal_chart(input_file):
    """
    Given a .csv file with smells and date columns, creates a temporal chart which
    highlights the number of smells between different dates/executions
    """
    df = pd.read_csv(input_file)

    df['date'] = pd.to_datetime(df['date'])

    df = df.sort_values('date')

    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['smells'], marker='o', linestyle='-')
    plt.title('Number of Smells Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Smells')

    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.grid(True)

    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Generate a temporal chart of smells over time")
    parser.add_argument('--input', type=str, required=True, help="Path to the input .csv file")

    args = parser.parse_args()

    temporal_chart(args.input)


if __name__ == "__main__":
    main()