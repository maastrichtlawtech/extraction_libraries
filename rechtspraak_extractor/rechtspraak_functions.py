import requests, glob, time, logging
from pathlib import Path
import pandas as pd


# Check whether the API is working or not and return with the response code
def check_api(url):
    response = requests.get(f"{url}")

    # Return with the response code
    return response.status_code


# Reads all the CSV files in a folder and returns the list of files
# It also has an optional parameter "exclude". By default, it's None. If you want to exclude files having a certain
# word in the file name, you may give a value
# It also only grabs data if it has rechtspraak in it
# As that was causing issues with other csv data present
def read_csv(dir_name, exclude=None):
    path = dir_name
    csv_files = glob.glob(path + "/*.csv")
    files = []
    for i in csv_files:
        if exclude is not None:
            if exclude not in i and "rechtspraak" in i:
                files.append(i)
        else:
            if "rechtspraak" in i:
                files.append(i)

    logging.info("Found " + str(len(files)) + " CSV file(s)\n")
    return files


# Get total execution time
def get_exe_time(start_time):
    end_time = time.time()
    sec = end_time - start_time
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    logging.info("Total execution time: {0}:{1}:{2}".format(int(hours), int(mins), round(sec, 2)))
    logging.info("\n")
