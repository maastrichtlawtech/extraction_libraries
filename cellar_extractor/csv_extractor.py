import glob
import argparse
import logging
from cellar_extractor.json_to_csv import read_csv


def extract_rows(data, number):
    """
    Method takes in a dataframe and returns a dataframe
    with only *number* of data rows.
    """

    try:
        output = data[1:number]
    except Exception:
        logging.info(f"The file does not have {number} entries,\
                     returning entire file.")
        output = data
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--amount", help="number of rows to extract", type=int, required=True
    )
    args = parser.parse_args()
    number = args.amount
    print("")
    print("EXTRACTION FROM CSV FILE IN DATA PROCESSED DIR STARTED")
    print("")
    DIR_DATA_RAW = ""
    csv_files = glob.glob(DIR_DATA_RAW + "/" + "*.csv")
    print(f"FOUND {len(csv_files)} CSV FILES")

    for i in range(len(csv_files)):
        # Approach for manual extraction of a specific file in a
        # specific directory
        if "clean" not in csv_files[i]:
            print("")
            print(f"EXTRACTING FROM {csv_files[i]} ")
            data = read_csv(csv_files[i])
            output = extract_rows(data, number)
            output_path = "/tester_100.csv"
            output.to_csv(output_path, index=False)
    print("")
    print("Extraction DONE")
    print("")
