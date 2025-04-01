import glob
import logging
import requests
import time


def check_api(url):
    """
    Check whether the API is working or not and return the response code.

    Args:
        url (str): The URL of the API to check.

    Returns:
        int: The HTTP response status code from the API.
    """

    response = requests.get(f"{url}")

    # Return with the response code
    return response.status_code


def read_csv(dir_name, exclude=None):
    """
    Reads all the CSV files in a folder and returns a list of files.

    Args:
        dir_name (str): The directory path containing the CSV files.
        exclude (str, optional): A word to exclude files containing it in
        their name. Defaults to None.

    Returns:
        list: A list of file paths for CSV files that match the criteria.

    Notes:
        - Only files with "rechtspraak" in their name are included.
        - If `exclude` is provided, files containing the `exclude` word in
        their name are excluded.
    """
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


def get_exe_time(start_time):
    """
    Calculate and log the total execution time.

    Args:
        start_time (float): The start time in seconds since the epoch.

    Logs:
        str: The total execution time in the format "hours:minutes:seconds".
    """
    end_time = time.time()
    sec = end_time - start_time
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    logging.info(
        "Total execution time: {0}:{1}:{2}".format(int(hours), int(mins),
                                                   round(sec, 2))
    )
    logging.info("\n")
