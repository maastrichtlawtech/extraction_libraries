# This file is used for getting the metadata of the ECLIs obtained using
# rechspraak_api file. This file takes all the
# CSV file created by rechspraak_api, picks up ECLIs and links column,
# and using an API gets the metadata and saves it
# in another CSV file with metadata suffix.
# This happens in async manner.

import logging
import multiprocessing
import os
import pandas as pd
import shutil
import time
import urllib

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
from pathlib import Path
from rechtspraak_extractor.rechtspraak_functions import (
    check_api,
    read_csv,
    get_exe_time,
)
from tqdm import tqdm

# Define base url
RECHTSPRAAK_METADATA_API_BASE_URL = "https://data.rechtspraak.nl/uitspraken/content?id="
# old one = "https://uitspraken.rechtspraak.nl/#!/details?id="
return_type = "&return=DOC"

# Dataframe with columns ecli, full_text, creator, date_decision, issued,
# zaaknummer, type, relations, references, subject, procedure,
# inhoudsindicatie, hasVersion
_columns = [
    "ecli",
    "full_text",
    "creator",
    "date_decision",
    "issued",
    "zaaknummer",
    "type",
    "relations",
    "references",
    "subject",
    "procedure",
    "inhoudsindicatie",
    "hasVersion",
]
temp_df = pd.DataFrame(columns=_columns)
_failed_eclis = []
threads = []
max_workers = 0
_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip,deflate,br,zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "data.rechtspraak.nl",
    "Upgrade-Insecure-Requests": "1",
}


def get_cores():
    """
    Determines the number of logical CPU cores available on the machine and
    sets the global variable `max_workers` to the number of cores minus one.
    This is useful for configuring the maximum number of concurrent processes
    or threads that can be run efficiently.

    Notes:
        - The `max_workers` value is calculated as the number of logical
        CPU cores minus one, assuming the main process is computationally
        intensive.
        - The function logs the maximum number of threads supported
        by the machine.

    Global Variables:
        max_workers (int): The maximum number of threads or processes
        that can be used concurrently.

    Logging:
        Logs the calculated `max_workers` value as an informational message.
    """
    n_cores = multiprocessing.cpu_count()

    global max_workers
    max_workers = n_cores - 1
    # If the main process is computationally intensive: Set to the number of
    # logical CPU cores minus one.

    logging.info(
        f"Maximum {str(max_workers)} threads supported by\
                  your machine."
    )


def extract_data_from_xml(url):
    _request = urllib.request.Request(url, headers=_headers)
    with urllib.request.urlopen(_request) as response:
        xml_file = response.read()
        return xml_file


def check_if_df_empty(df):
    if df.empty:
        return True
    return False


def get_text_if_exists(el, ecli):
    global _failed_eclis
    try:
        return el.text
    except Exception as e:
        _failed_eclis.append(ecli)
        logging.log(
            logging.WARNING,
            f"An error occurred while getting\
            the metadata of ECLI: {ecli} with error: {e} for tag: {el}",
        )
        return ""


def update_bar(bar, *args):
    bar.update(1)


def save_data_when_crashed(ecli):
    global temp_df
    # Append the dataframe temp_df with empty values
    temp_df.loc[len(temp_df)] = [ecli] + [""] * (len(_columns) - 1)


def get_data_from_api(ecli_id):
    global temp_df
    url = f"{RECHTSPRAAK_METADATA_API_BASE_URL}{ecli_id}&return=DOC"
    try:
        response_code = check_api(url)
    except Exception as e:
        logging.warning(
            f"An exception occurred while getting\
                the metadata of ECLI: {ecli_id} with error: {e}"
        )
        save_data_when_crashed(ecli_id)
        return
    try:
        if response_code == 200:
            try:
                # Extract data from xml
                xml_object = extract_data_from_xml(url)
                soup = BeautifulSoup(xml_object, features="xml")
                metadata_fields = {
                    "creator": "dcterms:creator",
                    "date_decision": "dcterms:date",
                    "issued": "dcterms:issued",
                    "zaaknummer": "psi:zaaknummer",
                    "type": "dcterms:type",
                    "subject": "dcterms:subject",
                    "relations": "dcterms:relation",
                    "references": "dcterms:references",
                    "procedure": "psi:procedure",
                    "inhoudsindicatie": "inhoudsindicatie",
                    "hasVersion": "dcterms:hasVersion",
                    "full_text": "uitspraak",
                }
                metadata_dict = {}
                for field, tag in metadata_fields.items():
                    if soup.find(tag) is not None:
                        value = get_text_if_exists(soup.find(tag), ecli_id)
                        if field == "relations" or field == "references":
                            # Handle multiple values for relations
                            # and references
                            items = soup.find_all(tag)
                            combined_value = ""
                            for item in items:
                                text = get_text_if_exists(item, ecli_id)
                                if text:
                                    combined_value += text + "\n"
                            value = combined_value.strip()
                        metadata_dict[field] = value
                # Append the dataframe temp_df with the metadata
                metadata_dict["ecli"] = ecli_id
                temp_df.loc[len(temp_df)] = [
                    metadata_dict.get(col, "") for col in _columns
                ]
                del metadata_dict

                urllib.request.urlcleanup()

            except Exception as e:
                logging.warning(
                    f"An error occurred while getting the metadata of ECLI:\
                        {ecli_id} with error: {e}"
                )
                save_data_when_crashed(ecli_id)
        else:
            save_data_when_crashed(ecli_id)
    except Exception as e:
        logging.warning(
            f"An error occurred while getting the metadata of ECLI: {ecli_id}\
                with error: {e}"
        )
        save_data_when_crashed(ecli_id)


def get_rechtspraak_metadata(save_file="n", dataframe=None, filename=None):
    global temp_df, _failed_eclis
    if dataframe is not None and filename is not None:
        logging.warning(
            "Please provide either a dataframe or a filename,\
                         but not both"
        )
        return False

    if dataframe is None and filename is None and save_file == "n":
        logging.warning(
            'Please provide at least a dataframe of filename\
                        when the save_file is "n"'
        )
        return False

    logging.info("Starting extraction with Rechtspraak metadata API")
    start_time = time.time()  # Get start time
    no_of_rows = ""
    rs_data = ""
    csv_files = 0

    # Check if dataframe is provided and is correct
    if dataframe is not None:
        if "id" in dataframe and "link" in dataframe:
            rs_data = dataframe
            no_of_rows = rs_data.shape[0]
        else:
            logging.info(
                "Dataframe is corrupted or does not contain\
                         necessary information to get the metadata."
            )
            return False

    # Check if filename is provided and is correct
    if filename is not None:
        logging.info("Reading " + filename + " from data folder")
        file_check = Path("data/" + filename)
        if file_check.is_file():
            logging.info("File found. Checking if metadata already exists")
            # Check if metadata already exists
            file_check = Path(
                "data/"
                + filename.split("/")[-1][: len(filename.split("/")[-1]) - 4]
                + "_metadata.csv"
            )
            if file_check.is_file():
                logging.info(
                    "Metadata for "
                    + filename.split("/")[-1][: len(filename.split("/")[-1]) - 4]
                    + ".csv already exists."
                )
                return False
            else:
                rs_data = pd.read_csv("data/" + filename)
                if "id" in rs_data and "link" in rs_data:
                    no_of_rows = rs_data.shape[0]
                else:
                    logging.warning(
                        "File is corrupted or does not contain\
                                    necessary information to get the metadata."
                    )
                    return False
        else:
            logging.info("File not found. Please check the file name.")
            return False

    get_cores()  # Get number of cores supported by the CPU

    if dataframe is None and filename is None and save_file == "y":
        logging.info(
            "No dataframe or file name is provided. Getting the metadata\
                of all the files present in the data folder"
        )

        logging.info("Reading all CSV files in the data folder...")
        csv_files = read_csv("data", "metadata")

        if len(csv_files) > 0 and save_file == "y":
            for f in csv_files:
                # Create empty dataframe
                rsm_df = pd.DataFrame(columns=_columns)
                temp_file_name = os.path.basename(f).replace(".csv", "")

                # Check if file already exists
                file_check = Path("data/" + temp_file_name + "_metadata.csv")
                if file_check.is_file():
                    logging.info(
                        f"Metadata for {temp_file_name}.csv\
                                 already exists."
                    )
                    continue

                rs_data = pd.read_csv(f)
                no_of_rows = rs_data.shape[0]
                logging.info(
                    "Getting metadata of "
                    + str(no_of_rows)
                    + " ECLIs from "
                    + temp_file_name
                    + ".csv"
                )
                logging.info("Working. Please wait...")

                if rs_data.empty:
                    print("It is empty")
                    logging.error(
                        "The DataFrame is empty. Please check the input data."
                    )
                    return False

                logging.info(
                    f"Available columns in the DataFrame:\
                        {rs_data.columns.tolist()}"
                )
                if "id" not in rs_data.columns:
                    print(
                        f"it is not empty but has columns\
                           {rs_data.columns.tolist()}"
                    )
                    logging.error(
                        "'id' column is missing in the DataFrame.\
                              Please check the input data."
                    )
                    return False

                # Get all ECLIs in a list
                ecli_list = list(rs_data.loc[:, "id"])

                # Create a temporary directory to save files
                time.sleep(1)
                Path("temp_rs_data").mkdir(parents=True, exist_ok=True)
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    bar = tqdm(
                        total=len(ecli_list),
                        colour="GREEN",
                        position=0,
                        leave=True,
                        miniters=int(len(ecli_list) / 100),
                        maxinterval=10000,
                    )
                    futures = {
                        executor.submit(get_data_from_api, ecli): ecli
                        for ecli in ecli_list
                    }
                    for future in futures:
                        future.add_done_callback(partial(update_bar, bar))

                # Delete temporary directory
                shutil.rmtree("temp_rs_data")
                # executor.shutdown()  # Shutdown the executor
                rsm_df = temp_df
                addition = rs_data[["id", "summary"]]
                rsm_df = rsm_df.merge(
                    addition, how="left", left_on="ecli", right_on="id"
                ).drop(["id"], axis=1)
                # Create directory if not exists
                Path("data").mkdir(parents=True, exist_ok=True)

                if check_if_df_empty(rsm_df):
                    logging.warning(
                        "Metadata not found. Please check the API response;\
                            either API is under maintenance, "
                        "experiencing problems, or has changed.\
                              Please try again after some time or contact the "
                        "administrator.\n"
                    )
                else:
                    # Save CSV file
                    logging.info("Creating CSV file...")
                    rsm_df.to_csv(
                        "data/" + temp_file_name + "_metadata.csv",
                        index=False,
                        encoding="utf8",
                    )
                    logging.info(
                        "CSV file "
                        + temp_file_name
                        + "_metadata.csv  successfully created.\n"
                    )
                # Check if any ECLI failed
                if len(_failed_eclis) > 0:
                    logging.warning(
                        "The following ECLIs failed to get metadata: "
                        + str(_failed_eclis)
                    )
                    # Store it in a file
                    with open(
                        "data/" + temp_file_name + "_failed_eclis.txt",
                        "w",
                    ) as f:
                        for ecli in _failed_eclis:
                            f.write(ecli + "\n")
                del rsm_df, temp_df, _failed_eclis
            return True

    if rs_data is not None:
        rsm_df = pd.DataFrame(columns=_columns)

        logging.info("Getting metadata of " + str(no_of_rows) + " ECLIs")
        logging.info("Working. Please wait...")
        # Get all ECLIs in a list
        ecli_list = list(rs_data.loc[:, "id"])

        # Create a temporary directory to save files
        Path("temp_rs_data").mkdir(parents=True, exist_ok=True)
        time.sleep(1)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            bar = tqdm(
                total=len(ecli_list),
                colour="GREEN",
                position=0,
                leave=True,
                miniters=int(len(ecli_list) / 100),
                maxinterval=10000,
            )
            for ecli in ecli_list:
                threads.append(executor.submit(get_data_from_api, ecli))
            for t in threads:
                t.add_done_callback(partial(update_bar, bar))
        # Delete temporary directory
        shutil.rmtree("temp_rs_data")
        # to finish unfinished?
        rsm_df = temp_df
        addition = rs_data[["id", "summary"]]
        rsm_df = rsm_df.merge(addition, how="left", left_on="ecli", right_on="id").drop(
            ["id"], axis=1
        )
        if save_file == "y":
            if filename is None or filename == "":
                filename = (
                    "custom_rechtspraak_" + datetime.now().strftime("%H-%M-%S") + ".csv"
                )
            # Create directory if not exists
            Path("data").mkdir(parents=True, exist_ok=True)

            if check_if_df_empty(rsm_df):
                logging.warning(
                    "Metadata not found. Please check the API response;\
                        either API is under maintenance, "
                    "experiencing problems, or has changed.\
                          Please try again after some time or contact the "
                    "administrator.\n"
                )
            else:
                # Save CSV file
                logging.info("Creating CSV file...")
                rsm_df.to_csv(
                    "data/"
                    + filename.split("/")[-1][: len(filename.split("/")[-1]) - 4]
                    + "_metadata.csv",
                    index=False,
                    encoding="utf8",
                )
                logging.info(
                    "CSV file "
                    + filename.split("/")[-1][: len(filename.split("/")[-1]) - 4]
                    + "_metadata.csv"
                    + " successfully created.\n"
                )
        # Check if any ECLI failed
        if len(_failed_eclis) > 0:
            logging.warning(
                "The following ECLIs failed to get metadata: " + str(_failed_eclis)
            )
            # Store it in a file
            with open(
                "data/"
                + filename.split("/")[-1][: len(filename.split("/")[-1]) - 4]
                + "_failed_eclis.txt",
                "w",
            ) as f:
                for ecli in _failed_eclis:
                    f.write(ecli + "\n")
        get_exe_time(start_time)

        if save_file == "n":
            return rsm_df
        del temp_df, _failed_eclis
        return True
