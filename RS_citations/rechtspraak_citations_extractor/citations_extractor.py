import json
import threading
import time
import urllib.request
import logging
import pandas as pd
import rdflib
import requests
# from dotenv import load_dotenv
from lxml import etree
from requests.auth import HTTPBasicAuth
from tqdm import tqdm
import re

# load_dotenv()

LIDO_ENDPOINT = "http://linkeddata.overheid.nl/service/get-links"

target_ecli = 'target_ecli'
label = 'label'
type = 'type'
ecli = 'ecli'
case_citations_fieldnames = [target_ecli, label, type]
legislation_citations_fieldnames = ['legal_provision_url_lido', 'legal_provision_url', 'legal_provision']


def remove_spaces_from_ecli(ecli):
    return ecli.replace(" ", "")


def write_incremental_rows(filename, data):
    with open(filename, 'a') as f:
        pd.DataFrame(data).to_csv(f, mode='a', header=not f.tell(), index=False)


# Code to execute LIDO API call
def get_lido_response(url, username, password):
    authentication = HTTPBasicAuth(username, password)
    response = requests.get(url, auth=authentication)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception('LinkedData responded with code {}: {}. {}'.format(response.status_code, response.reason, url))


# Extract the ECLI code from the LIDO identifier of the cited case law from the XML response from LIDO API
def get_ecli(sub_ref):
    return sub_ref.attrib['idref'].split('/')[-1]


# Extract the LIDO identifier of the cited legislation from the XML response from LIDO API
def get_legislation_identifier(sub_ref):
    return sub_ref.attrib['idref']


# Find the webpage expressing, in writing, the legislation referred to by the input LIDO identifier
def get_legislation_webpage(identifier):
    idcomponents = identifier.split("/")
    date = idcomponents[len(idcomponents) - 1]
    url = identifier
    page = urllib.request.urlopen(url)
    g = rdflib.Graph()
    g.parse(page, format="xml")
    article = ""
    for s, p, o in g:
        if str(p) == "http://purl.org/dc/terms/identifier":
            article = o
            if date in str(o):
                return o

    return article


def get_legislation_name(url, username, password):
    # turn the response into an xml tree
    xml_response = get_lido_response(url, username, password)
    xml = etree.fromstring(bytes(xml_response, encoding='utf8'))

    pref_label = ""
    title = ""
    # RDF main element (root)
    for element in xml.iterchildren():
        # there is only one child and it is the "description" in which the rest of the info is
        # go through all the tags (all the info)
        for el in element.iterchildren():
            # the title (same thing as the preLabel) is the feature we want to be using
            if el.tag == "{http://purl.org/dc/terms/}title":
                title = el.text

    return title


# Check if outgoing links in the XML response from the LIDO API are of type "Jurisprudentie" (case law)
def is_case_law(sub_ref):
    return sub_ref.attrib['groep'] == 'Jurisprudentie'


# Check if outgoing links in the XML response from the LIDO API are of type "Wet" (legislation)
def is_legislation(sub_ref):
    return sub_ref.attrib['groep'] == 'Wet' or sub_ref.attrib['groep'] == 'Artikel'


# Extract ECLI code of citation from a lido identifier.
# Example of a LIDO identifier "https://linkeddata.overheid.nl/terms/bwb/id/BWBR0020368/8655654/2016-08-11/2016-08-11"
def get_lido_id(ecli):
    return "http://linkeddata.overheid.nl/terms/jurisprudentie/id/" + ecli


# Method written by Marion
"""
These methods are used to write the citations incrementally to the csv file (in case it crashes or times out). 
It allows us to stop the script whenever we want without loosing our data, and without having to start from the bginning the next time. 
"""


def citations_multithread_single(big_incoming, big_outgoing, big_legislations, ecli, username, password, current_index,
                                 bar):
    incoming_df = pd.Series([], dtype='string')
    outgoing_df = pd.Series([], dtype='string')
    legislations_df = pd.Series([], dtype='string')
    for i, ecli in enumerate(ecli):
        index = current_index + i
        case_citations_incoming, case_citations_outgoing, legislation_citations = find_citations_for_case_retrying(0,
            remove_spaces_from_ecli(ecli), case_citations_fieldnames, legislation_citations_fieldnames, username,
            password)
        if case_citations_incoming:
            encoded = json.dumps(case_citations_incoming)
            incoming_df[index] = encoded
        if case_citations_outgoing:
            encoded = json.dumps(case_citations_outgoing)
            outgoing_df[index] = encoded
        if legislation_citations:
            encoded = json.dumps(legislation_citations)
            legislations_df[index] = encoded
        bar.update(1)
    big_incoming.append(incoming_df)
    big_outgoing.append(outgoing_df)
    big_legislations.append(legislations_df)


def add_column_frow_list(data, name, list):
    column = pd.Series([], dtype='string')
    for l in list:
        column = column._append(l)
    column.sort_index(inplace=True)
    data.insert(1, name, column)


def find_citations_for_cases_multithread(dataframe, username, password, threads):
    ecli = dataframe['ecli'].dropna().reset_index(drop=True)
    length = ecli.size
    at_once_threads = int(length / threads)
    big_incoming = []
    big_outgoing = []
    big_legislations = []
    threads = []
    bwb_list = []
    bar = tqdm(total=length, colour="GREEN", position=0, leave=True, miniters=int(length / 100), maxinterval=10000)

    for i in range(0, length, at_once_threads):
        curr_ecli = ecli[i:(i + at_once_threads)]
        t = threading.Thread(target=citations_multithread_single,
                             args=[big_incoming, big_outgoing, big_legislations, curr_ecli, username, password, i, bar])
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    add_column_frow_list(dataframe, 'citations_incoming', big_incoming)
    add_column_frow_list(dataframe, 'citations_outgoing', big_outgoing)
    add_column_frow_list(dataframe, 'legislations_cited', big_legislations)
    # Iterate over big_legislations and find bwb_ids using regular expressions
    for leg_citations in big_legislations:
        for leg_citation in leg_citations:
            match = re.search(r"bwb/id/([^/]+)", leg_citation)
            if match:
                bwb_list.append(match.group(1))
            else:
                bwb_list.append(None)
    dataframe['bwb_id'] = pd.Series(bwb_list)

    return dataframe


def add_citations_no_duplicates(already_existing_list, element):
    duplicate = False
    new_ecli = get_ecli(element)
    added_sth_new = True
    for stored in already_existing_list:
        if stored[target_ecli] == new_ecli:
            added_sth_new = False
            duplicate = True
            break
    if not duplicate:
        already_existing_list.append({target_ecli: new_ecli,
                                      label: element.attrib['label'],
                                      type: element.attrib['type'].split('/id/')[1]})
    return added_sth_new


def add_legislations_no_duplicates(list, element):
    duplicate = False
    new_legislation = get_legislation_identifier(element)
    added_sth_new = True
    for legs in list:
        if new_legislation == legs:
            added_sth_new = False
            duplicate = True
            break
    if not duplicate:
        list.append(get_legislation_identifier(element))
    return added_sth_new



def find_citations_for_case_retrying(retry, *args):
    if retry == 5:
        return False, False, False
    else:
        time.sleep(2 * retry)
    try:
        return find_citations_for_case(*args)
    except:
        return find_citations_for_case_retrying(retry + 1, *args)

# Main method to execute LIDO API call on the ECLI code of the input case and extract the citations
def find_citations_for_case(ecli, case_citations_fieldnames, legislation_citations_fieldnames, username, password):
    xml_elements = []
    case_law_citations_outgoing = []
    legislation_citations = []
    case_law_citations_incoming = []
    start_page = 0
    end_of_pages = False
    outgoing = "uitgaande-links"
    incoming = "inkomende-links"

    while not end_of_pages:
        added_sth_new = False
        url = "{}?id={}&start={}&rows={}&output=xml".format(LIDO_ENDPOINT, get_lido_id(ecli), start_page, 10)
        start_page += 1

        xml_text = get_lido_response(url, username, password)
        xml_elements.append(etree.fromstring(xml_text.encode('utf8')))

        for el in xml_elements:
            for sub in list(el.iterchildren('subject')):

                for the_citations in sub.iterchildren(outgoing):
                    for sub_ref in the_citations.iterchildren():
                        if is_case_law(sub_ref):
                            added_sth_new = add_citations_no_duplicates(case_law_citations_outgoing, sub_ref)
                        elif is_legislation(sub_ref):
                            added_sth_new = add_legislations_no_duplicates(legislation_citations, sub_ref)

                for the_citations in sub.iterchildren(incoming):
                    for sub_ref in the_citations.iterchildren():
                        if is_case_law(sub_ref):
                            added_sth_new = add_citations_no_duplicates(case_law_citations_incoming, sub_ref)

        if not added_sth_new or start_page > 15:
            # print(start_page)
            end_of_pages = True

    # Remove duplicates empties

    for item in case_law_citations_incoming:
        if item[target_ecli] == "":
            case_law_citations_incoming.remove(item)
    for item in case_law_citations_outgoing:
        if item[target_ecli] == "":
            case_law_citations_outgoing.remove(item)

    # Remove input case ECLI (for some reason a case can cite itself...)
    for dicts in case_law_citations_incoming:
        if dicts[target_ecli] == remove_spaces_from_ecli(ecli):
            case_law_citations_incoming.remove(dicts)
            break
    for dicts in case_law_citations_outgoing:
        if dicts[target_ecli] == remove_spaces_from_ecli(ecli):
            case_law_citations_outgoing.remove(dicts)
            break
    if (remove_spaces_from_ecli(ecli) in case_law_citations_incoming):
        case_law_citations_incoming.remove(remove_spaces_from_ecli(ecli))

    case_law_result_outgoing = extract_results_citations(case_law_citations_outgoing, ecli, case_citations_fieldnames)
    case_law_results_incoming = extract_results_citations(case_law_citations_incoming, ecli, case_citations_fieldnames)
    legislation_results = extract_results_legislations(legislation_citations, ecli, legislation_citations_fieldnames,
                                                       username, password)
    
    return case_law_results_incoming, case_law_result_outgoing, legislation_results


def extract_results_citations(list, ecli, fields):
    list_of_all_results = []

    for case_citation in list:
        case_law_result = {key: None for key in fields}
        case_law_result[fields[0]] = (remove_spaces_from_ecli(case_citation[target_ecli]))  # Target ECLI
        case_law_result[fields[1]] = (case_citation['label'])  # Target ECLI
        case_law_result[fields[2]] = (case_citation['type'])  # Target ECLI
        list_of_all_results.append(case_law_result)
    return list_of_all_results


def extract_results_legislations(list, ecli, fields, username, password):
    list_of_all_results = []
    for leg_citation in list:
        legislation_result = {key: None for key in fields}
        legislation_result[fields[0]] = (leg_citation)  # Target article
        legislation_result[fields[1]] = (get_legislation_webpage(leg_citation))  # Target article webpage
        legislation_result[fields[2]] = (
            get_legislation_name(leg_citation, username, password))  # pref label == article name
        list_of_all_results.append(legislation_result)
    return list_of_all_results


def get_citations(dataframe=None, username="", password="", threads=1):
    if dataframe is None or not username or not password:
        logging.warning("Incorrect arguments passed. Returning...")
        return False
    try:
        get_lido_response(LIDO_ENDPOINT, username, password)
    except:
        logging.warning('LIDO cannot be accessed with these login details. Returning...')
        return False
    logging.info('\n--- START OF RS CITATIONS EXTRACTIONS ---\n')

    # find citations, and save the file incrementally
    df = find_citations_for_cases_multithread(dataframe, username, password, threads)

    logging.info("\n--- DONE ---")
    return df
