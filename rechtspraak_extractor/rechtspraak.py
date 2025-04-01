# This file is used to get all the Rechtspraak ECLIs from an API.
# It takes two required arguments and one optional argument
# 1. max - Maximum number of ECLIs to retrieve
# 2. starting-date (yyyy-mm-dd) - Start date of ECLI publication
# 3. ending-date (yyyy-mm-dd) - It's an optional parameter. If not given,
# current date will be automatically chosen
# File is stored in data/rechtspraak folder

import json
import xmltodict
import logging
import re
import time
import requests
import pandas as pd

from datetime import date, datetime
from pathlib import Path
from rechtspraak_extractor.rechtspraak_functions import check_api, get_exe_time


# Define base URL
RECHTSPRAAK_API_BASE_URL = "https://data.rechtspraak.nl/uitspraken/zoeken?"


def get_data_from_url(base_url, total_docs, start_date, end_date):
    all_results = []
    from_index = 0
    max_ecli_per_page = 1000
    while True:
        url = (base_url +
               'max=' + str(max_ecli_per_page) +
               '&from=' + str(from_index) +
               '&date=' + str(start_date) +
               '&date=' + str(end_date)
               )
        res = requests.get(url)
        res.raw.decode_content = True
        # Convert the XML data to JSON format
        xpars = xmltodict.parse(res.text)
        json_string = json.dumps(xpars)
        json_object = json.loads(json_string)
        # print(json_object['feed']['entry'])
        # Update the all_results object with the new data
        all_results.extend(json_object['feed']['entry'])
        logging.info(f"Retrieved {len(json_object['feed']['entry'])}\
                     cases (total: {len(all_results)})")

        if len(all_results) >= total_docs:
            logging.info("Maximum number of ECLIs reached")
            break
        from_index += max_ecli_per_page
        time.sleep(1)

    return all_results


def _num_of_available_docs(url, start_date, end_date, amount, from_index=0):
    _url = (url +
            'max=' + str(amount) +
            '&from=' + str(from_index) +
            '&date=' + str(start_date) +
            '&date=' + str(end_date)
            )
    response = requests.get(_url)
    response.raw.decode_content = True
    xpars = xmltodict.parse(response.text)
    json_string = json.dumps(xpars)
    json_object = json.loads(json_string)
    return int(re.search(r'\d+',
                         json_object['feed']['subtitle']['#text']).group())


def save_csv(json_object, file_name, save_file):
    # Define the dataframe to enter the data
    df = pd.DataFrame(columns=['id', 'title', 'summary', 'updated', 'link'])
    ecli_id = []
    title = []
    summary = []
    updated = []
    link = []

    # Iterate over the object and fill the lists
    for i in json_object:
        ecli_id.append(i['id'])
        title.append(i['title']['#text'])
        if '#text' in i['summary']:
            summary.append(i['summary']['#text'])
        else:
            summary.append("No summary available")
        updated.append(i['updated'])
        link.append(i['link']['@href'])

    # Save the lists to dataframe
    df['id'] = ecli_id
    df['title'] = title
    df['summary'] = summary
    df['updated'] = updated
    df['link'] = link

    if save_file == 'y':
        # Create directory if not exists
        Path('data').mkdir(parents=True, exist_ok=True)

        # Save CSV file
        # file_path = os.path.join('data', file_name + '.csv')
        df.to_csv('data/' + file_name + '.csv', index=False, encoding='utf8')
        logging.info("Data saved to CSV file successfully.")
    return df


def get_rechtspraak(max_ecli=1000, sd='1900-01-01', ed=None, save_file='y'):
    logging.info("Rechtspraak dump downloader API")
    starting_date = sd
    save_file = save_file

    # If the end date is not entered, the current date is taken
    today = date.today()
    if ed:
        ending_date = ed
    else:
        ending_date = today.strftime("%Y-%m-%d")

    # Used to calculate total execution time
    start_time = time.time()

    # Build the URL after getting all the arguments
    url = (RECHTSPRAAK_API_BASE_URL +
           'max=' + str(max_ecli) +
           '&from=0' +
           '&date=' + starting_date +
           '&date=' + ending_date)

    logging.info("Checking the API")
    # Check the working of API
    response_code = check_api(url)
    if response_code == 200:
        logging.info("API is working fine!")
        # Check the number of documents available for retrieval
        logging.info("Checking the number of documents available")
        total_docs = _num_of_available_docs(RECHTSPRAAK_API_BASE_URL,
                                            starting_date,
                                            ending_date,
                                            max_ecli)
        if max_ecli != total_docs:
            logging.info(f"Total available number of documents is {total_docs}\
                         but will fetch only {max_ecli}")
            total_docs = max_ecli
        logging.info(f"Total number of documents for retrieval:{total_docs}")
        logging.info("Getting " + str(max_ecli) + " documents from " +
                     starting_date + " till " + ending_date)
        json_object = get_data_from_url(RECHTSPRAAK_API_BASE_URL, total_docs,
                                        starting_date, ending_date)
        logging.info(f"Found {len(json_object)} cases!")
        if json_object:
            # Get current time
            current_time = datetime.now().strftime("%H-%M-%S")

            # Build file name
            file_name = 'rechtspraak_' + starting_date + '_' +\
                ending_date + '_' + current_time
            get_exe_time(start_time)

            if save_file == 'n':
                global_rs_df = save_csv(json_object, file_name, save_file)
                return global_rs_df
            else:
                save_csv(json_object, file_name, save_file)
                return
    else:
        logging.info(f"URL returned with a {response_code} error code")
