import argparse
import sys
import pandas as pd




def smell_report(input_file):
    df = pd.read_csv(input_file)
    #filter dataframe with only the columns we need
    df = df[[ 'name_smell', 'smell']]
    a = df.groupby('name_smell').sum()
    a.to_csv('general_overview.csv')

def project_report(input_file):
    df = pd.read_csv(input_file)
    #filter dataframe with only the columns we need
    df = df[['filename', 'name_smell', 'smell']]
    #cut first part of filename to get project name
    df['project_name'] = df['filename'].str.extract(r'projects[\\/](.*?)[\\/]', expand=False)
    df = df[['project_name', 'smell']]
    # set dtype of smell as int
    df['smell'] = df['smell'].astype(int)
    a = df.groupby('project_name').sum()
    a.to_csv('project_overview.csv')
def main():
    parser = argparse.ArgumentParser(description="Generate a ausiliary charts ")
    parser.add_argument('--input', type=str, default="./overview_output.csv", help="Path to the input .csv file")

    args = parser.parse_args()
    project_report(args.input)
    smell_report(args.input)

    print("Ausiliary charts generated")
    sys.exit(0)

if __name__ == '__main__':
    main()
