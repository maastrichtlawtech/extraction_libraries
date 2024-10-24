# This file is used for getting the metadata of the ECLIs obtained using rechspraak_api file. This file takes all the
# CSV file created by rechspraak_api, picks up ECLIs and links column, and using an API gets the metadata and saves it
# in another CSV file with metadata suffix.
# This happens in async manner.
import pathlib
import os
import urllib
import multiprocessing
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import platform
import shutil
from tqdm import tqdm
from rechtspraak_extractor.rechtspraak_functions import *
from functools import partial
# Define base url
RECHTSPRAAK_METADATA_API_BASE_URL = "http://data.rechtspraak.nl/uitspraken/content?id=" # old one = "https://uitspraken.rechtspraak.nl/#!/details?id="
return_type = "&return=DOC"

# Define empty lists where we'll store our data temporarily
ecli_df = []
full_text_df = []
creator_df = []
date_decision_df = []
issued_df = []
zaaknummer_df = []
type_df = []
relations_df = []
references_df = []
subject_df = []
procedure_df = []
inhoudsindicatie_df = []
hasVersion_df = []

threads = []
max_workers = 0


def get_cores():
    # max_workers is the number of concurrent processes supported by your CPU multiplied by 5.
    # You can change it as per the computing power.
    # Different python versions treat this differently. This is written as per python 3.6.
    n_cores = multiprocessing.cpu_count()

    global max_workers
    max_workers = n_cores-1
    # If the main process is computationally intensive: Set to the number of logical CPU cores minus one.

    print(f"Maximum " + str(max_workers) + " threads supported by your machine.")


def extract_data_from_xml(url):
    with urllib.request.urlopen(url) as response:
        xml_file = response.read()
        return xml_file



def check_if_df_empty(df):
    if df.empty:
        return True
    return False


def get_text_if_exists(el):
    try:
        return el.text
    except:
        return ''

def update_bar(bar, *args):
    bar.update(1)


def save_data_when_crashed(ecli):
    ecli_df.append(ecli)
    full_text_df.append("")
    creator_df.append("")
    date_decision_df.append("")
    issued_df.append("")
    zaaknummer_df.append("")
    type_df.append("")
    relations_df.append("")
    references_df.append("")
    subject_df.append("")
    procedure_df.append("")
    inhoudsindicatie_df.append("")
    hasVersion_df.append("")
def get_data_from_api(ecli_id):
    url = RECHTSPRAAK_METADATA_API_BASE_URL + ecli_id + return_type
    try:
        response_code = check_api(url)
    except:
        save_data_when_crashed(ecli_id)
        return
    global ecli_df, full_text_df, creator_df, date_decision_df, issued_df, zaaknummer_df, type_df, \
        relations_df, references_df, subject_df, procedure_df, inhoudsindicatie_df, hasVersion_df
    try:
        if response_code == 200:
            try:
                # Extract data from xml
                xml_object = extract_data_from_xml(url)
                soup = BeautifulSoup(xml_object, features='xml')
                # Get the data
                creator = get_text_if_exists(soup.find("dcterms:creator"))
                date_decision = get_text_if_exists(soup.find("dcterms:date"))
                issued = get_text_if_exists(soup.find("dcterms:issued"))
                zaaknummer = get_text_if_exists(soup.find("psi:zaaknummer"))
                rs_type = get_text_if_exists(soup.find("dcterms:type"))
                subject = get_text_if_exists(soup.find("dcterms:subject"))
                relation = soup.findAll("dcterms:relation")
                relatie = ''
                for i in relation:
                    # append the string to relation
                    text = get_text_if_exists(i)
                    if text == '':
                        continue
                    else:
                        relatie += text + "\n"
                relations = relatie
                reference = soup.findAll("dcterms:references")
                ref = ''
                for u in reference:
                    text = get_text_if_exists(u)
                    # append the string to relation
                    if text =="":
                        continue
                    else:
                        ref += text + "\n"
                references = ref    
                procedure = get_text_if_exists(soup.find("psi:procedure"))
                inhoudsindicatie = get_text_if_exists(soup.find("inhoudsindicatie"))
                hasVersion = get_text_if_exists(soup.find("dcterms:hasVersion"))
                full_text = get_text_if_exists(soup.find("uitspraak"))

                ecli_df.append(ecli_id)
                full_text_df.append(full_text)
                creator_df.append(creator)
                date_decision_df.append(date_decision)
                issued_df.append(issued)
                zaaknummer_df.append(zaaknummer)
                type_df.append(rs_type)
                relations_df.append(relations)
                references_df.append(references)
                subject_df.append(subject)
                procedure_df.append(procedure)
                inhoudsindicatie_df.append(inhoudsindicatie)
                hasVersion_df.append(hasVersion)
                del full_text, creator, date_decision, issued, zaaknummer,relations, rs_type,\
                    references, subject,procedure, inhoudsindicatie, hasVersion

                urllib.request.urlcleanup()

            except Exception as e:
                save_data_when_crashed(ecli_id)
        else:
            save_data_when_crashed(ecli_id)
    except Exception as e:
        save_data_when_crashed(ecli_id)


def get_rechtspraak_metadata(save_file='n', dataframe=None, filename=None):
    if dataframe is not None and filename is not None:
        print(f"Please provide either a dataframe or a filename, but not both")
        return False

    if dataframe is None and filename is None and save_file == 'n':
        print(f"Please provide at least a dataframe of filename when the save_file is \"n\"")
        return False

    print("Rechtspraak metadata API")

    start_time = time.time()  # Get start time

    no_of_rows = ''
    rs_data = ''
    csv_files = 0

    # Check if dataframe is provided and is correct
    if dataframe is not None:
        if 'id' in dataframe and 'link' in dataframe:
            rs_data = dataframe
            no_of_rows = rs_data.shape[0]
        else:
            print("Dataframe is corrupted or does not contain necessary information to get the metadata.")
            return False

    # Check if filename is provided and is correct
    if filename is not None:
        print("Reading " + filename + " from data folder")
        file_check = pathlib.Path("data/" + filename)
        if file_check.is_file():
            print("File found. Checking if metadata already exists")
            # Check if metadata already exists
            file_check = Path("data/" + filename.split('/')[-1][:len(filename.split('/')[-1]) - 4]
                              + "_metadata.csv")
            if file_check.is_file():
                print("Metadata for " + filename.split('/')[-1][:len(filename.split('/')[-1]) - 4] +
                      ".csv already exists.")
                return False
            else:
                rs_data = pd.read_csv('data/' + filename)
                if 'id' in rs_data and 'link' in rs_data:
                    no_of_rows = rs_data.shape[0]
                else:
                    print("File is corrupted or does not contain necessary information to get the metadata.")
                    return False
        else:
            print("File not found. Please check the file name.")
            return False

    get_cores()  # Get number of cores supported by the CPU

    if dataframe is None and filename is None and save_file == 'y':
        print("No dataframe or file name is provided. Getting the metadata of all the files present in the "
              "data folder")

        print("Reading all CSV files in the data folder...")
        csv_files = read_csv('data', "metadata")

        global ecli_df, full_text_df, creator_df, date_decision_df, issued_df, zaaknummer_df, \
           type_df, relations_df,references_df, subject_df,\
           procedure_df, inhoudsindicatie_df, hasVersion_df
        if len(csv_files) > 0 and save_file == 'y':
            for f in csv_files:
                # Create empty dataframe
                rsm_df = pd.DataFrame(columns=['ecli', 'full_text', 'creator', 'date_decision',
                                               'issued', 'zaaknummer','type',"relations",
                                                'references','subject','procedure',
                                                'inhoudsindicatie', 'hasVersion'])

                temp_file_name = f.split('\\')[-1][:len(f.split('\\')[-1]) - 4]

                # Check if file already exists
                file_check = Path("data/" + temp_file_name + "_metadata.csv")
                if file_check.is_file():
                    print("Metadata for " + temp_file_name + ".csv already exists.")
                    continue

                df = pd.read_csv(f)
                no_of_rows = df.shape[0]
                print("Getting metadata of " + str(no_of_rows) + " ECLIs from " + temp_file_name + ".csv")
                print("Working. Please wait...")

                # Get all ECLIs in a list
                ecli_list = list(df.loc[:, 'id'])

                # Create a temporary directory to save files
                time.sleep(1)
                Path('temp_rs_data').mkdir(parents=True, exist_ok=True)
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    for ecli in ecli_list:
                        threads.append(executor.submit(get_data_from_api, ecli))

                # Delete temporary directory
                shutil.rmtree('temp_rs_data')
                # executor.shutdown()  # Shutdown the executor

                rsm_df['ecli'] = ecli_df
                rsm_df['full_text'] = full_text_df
                rsm_df['creator'] = creator_df
                rsm_df['date_decision'] = date_decision_df
                rsm_df['issued'] = issued_df
                rsm_df['zaaknummer'] = zaaknummer_df
                rsm_df['type'] = type_df
                rsm_df['relations'] = relations_df
                rsm_df['references'] = references_df
                rsm_df['subject'] = subject_df
                rsm_df['procedure'] = procedure_df
                rsm_df['inhoudsindicatie'] = inhoudsindicatie_df
                rsm_df['hasVersion'] = hasVersion_df
                addition = rs_data[['id', 'summary']]
                rsm_df = rsm_df.merge(addition, how='left', left_on='ecli', right_on='id').drop(['id'], axis=1)
                # Create directory if not exists
                Path('data').mkdir(parents=True, exist_ok=True)

                if check_if_df_empty(rsm_df):
                    print("Metadata not found. Please check the API response; either API is under maintenance, "
                          "experiencing problems, or has changed. Please try again after some time or contact the "
                          "administrator.\n")
                else:
                    # Save CSV file
                    print("Creating CSV file...")
                    rsm_df.to_csv("data/" + temp_file_name + "_metadata.csv", index=False, encoding='utf8')
                    print("CSV file " + temp_file_name + "_metadata.csv  successfully created.\n")

                # Clear the lists for the next file
                ecli_df = []
                full_text_df = []
                creator_df = []
                date_decision_df = []
                issued_df = []
                zaaknummer_df = []
                type_df = []
                relations_df = []
                references_df = []
                subject_df = []
                procedure_df = []
                inhoudsindicatie_df = []
                hasVersion_df = []
                ecli_list = []
                del rsm_df
            return True

    if rs_data is not None:
        rsm_df = pd.DataFrame(columns=['ecli', 'full_text', 'creator', 'date_decision', 'issued',
                                       'zaaknummer','type','relations','references', 'subject', 'procedure',
                                        'inhoudsindicatie','hasVersion'])

        print("Getting metadata of " + str(no_of_rows) + " ECLIs")
        print("Working. Please wait...")
        # Get all ECLIs in a list
        ecli_list = list(rs_data.loc[:, 'id'])

        # Create a temporary directory to save files
        Path('temp_rs_data').mkdir(parents=True, exist_ok=True)
        time.sleep(1)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            bar = tqdm(total=len(ecli_list), colour="GREEN",position=0, leave=True, miniters=int(len(ecli_list)/100),
                       maxinterval=10000)
            for ecli in ecli_list:
                threads.append(executor.submit(get_data_from_api, ecli))
            for t in threads:
                t.add_done_callback(partial(update_bar,bar))
        # Delete temporary directory
        shutil.rmtree('temp_rs_data')
         # to finish unfinished?
        # global ecli_df, full_text_df, creator_df, date_decision_df, issued_df, zaaknummer_df, \
        #    relations_df, subject_df, procedure_df, inhoudsindicatie_df, hasVersion_df

        rsm_df['ecli'] = ecli_df
        rsm_df['full_text'] = full_text_df
        rsm_df['creator'] = creator_df
        rsm_df['date_decision'] = date_decision_df
        rsm_df['issued'] = issued_df
        rsm_df['zaaknummer'] = zaaknummer_df
        rsm_df['type'] = type_df
        rsm_df['relations'] = relations_df
        rsm_df['references'] = references_df
        rsm_df['subject'] = subject_df
        rsm_df['procedure'] = procedure_df
        rsm_df['inhoudsindicatie'] = inhoudsindicatie_df
        rsm_df['hasVersion'] = hasVersion_df
        addition = rs_data[['id','summary']]
        rsm_df = rsm_df.merge(addition, how='left', left_on='ecli', right_on='id').drop(['id'], axis=1)
        if save_file == 'y':
            if filename is None or filename == '':
                filename = "custom_rechtspraak_" + datetime.now().strftime("%H-%M-%S") + ".csv"
            # Create directory if not exists
            Path('data').mkdir(parents=True, exist_ok=True)

            if check_if_df_empty(rsm_df):
                print("Metadata not found. Please check the API response; either API is under maintenance, "
                      "experiencing problems, or has changed. Please try again after some time or contact the "
                      "administrator.\n")
            else:
                # Save CSV file
                print("Creating CSV file...")
                rsm_df.to_csv("data/" + filename.split('/')[-1][:len(filename.split('/')[-1]) - 4] + "_metadata.csv",
                              index=False, encoding='utf8')
                print("CSV file " + filename.split('/')[-1][:len(filename.split('/')[-1]) - 4] + "_metadata.csv" +
                      " successfully created.\n")

        # Clear the lists for the next file
        ecli_df = []
        full_text_df = []
        creator_df = []
        date_decision_df = []
        issued_df = []
        zaaknummer_df = []
        type_df = []
        relations_df = []
        references_df = []
        subject_df = []
        procedure_df = []
        inhoudsindicatie_df = []
        hasVersion_df = []
        ecli_list = []

        get_exe_time(start_time)

        if save_file == 'n':
            return rsm_df

        return True

