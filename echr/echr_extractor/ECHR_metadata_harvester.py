import logging
from datetime import datetime

import pandas as pd
import requests


def get_r(url, timeout, retry, verbose):
    """
    Get data from a URL. If this is uncuccessful it is attempted again up to a number of tries
    given by retry. If it is still unsuccessful the batch is skipped.
    :param str url: The data source URL.
    :param double timeout: The amount of time to wait for a response each attempt.
    :param int retry: The number of times to retry upon failure.
    :param bool verbose: Whether or not to print extra information.
    """
    count = 0
    max_attempts = 20
    while count < max_attempts:
        try:
            r = requests.get(url, timeout=timeout)
            return r
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            count += 1
            if verbose:
                logging.info(f"Timeout. Retry attempt {count}.")
            if count > retry:
                if verbose:
                    logging.info(f"Unable to connect to {url}. Skipping this batch.")
                return None
    return None


def basic_function(term, values):
    values = ['"' + i + '"' for i in values]
    main_body = list()
    cut_term = term.replace('"', '')
    for v in values:
        main_body.append(f"({cut_term}={v}) OR ({cut_term}:{v})")
    query = f"({' OR '.join(main_body)})"
    return query


def link_to_query(link):
    # Fixing brackets
    link = link.replace('%7B', '{')
    link = link.replace('%7D', '}')
    link = link.replace('%5B', '[')
    link = link.replace('%5D', ']')
    link = link.replace('%22', '"')
    link = link.replace('%27', "'")

    # fixing fulltext shenanigans - happen because of people using " in the queries.

    full_text_input = ''
    fulltext_end = -1
    fulltext_start = link.find('fulltext')
    if fulltext_start:
        start = link[fulltext_start:].find('[') + fulltext_start + 1
        fulltext_end = link[fulltext_start:].find(']') + fulltext_start
        fragment_to_fix = link[start:fulltext_end]
        full_text_input = '(' + "".join(fragment_to_fix.rsplit('"', 1)).replace('"', "", 1) + ')'.replace('\\','')
        full_text_input = full_text_input.replace("\\",'')
        b=2
        # removing first and last " elements and saving the output to put manually later
    if (fulltext_end):

        if link[fulltext_end+1] == ',':
            to_replace = link[fulltext_start - 1:fulltext_end + 2]
        else:
            to_replace = link[fulltext_start - 1:fulltext_end + 1]
        link = link.replace(to_replace, '')

    extra_cases_map = {
        "bodyprocedure": '("PROCEDURE" ONEAR(n=1000) terms OR "PROCÉDURE" ONEAR(n=1000) terms)',
        "bodyfacts": '("THE FACTS" ONEAR(n=1000) terms OR "EN FAIT" ONEAR(n=1000) terms)',
        "bodycomplaints": '("COMPLAINTS" ONEAR(n=1000) terms OR "GRIEFS" ONEAR(n=1000) terms)',
        "bodylaw": '("THE LAW" ONEAR(n=1000) terms OR "EN DROIT" ONEAR(n=1000) terms)',
        "bodyreasons": '("FOR THESE REASONS" ONEAR(n=1000) terms OR "PAR CES MOTIFS" ONEAR(n=1000) terms)',
        "bodyseparateopinions": '(("SEPARATE OPINION" OR "SEPARATE OPINIONS") ONEAR(n=5000) terms OR "OPINION '
                                'SÉPARÉE" ONEAR(n=5000) terms)',
        "bodyappendix": '("APPENDIX" ONEAR(n=1000) terms OR "ANNEXE" ONEAR(n=1000) terms)'
    }

    def full_text_function(term, values):
        return f"({','.join(values)})"

    def date_function(term, values):
        values = ['"' + i + '"' for i in values]
        query = '(kpdate>=first_term AND kpdate<=second_term)'
        first = values[0]
        second = values[1]
        if first == '""':
            first = '"1900-01-01"'
        if second == '""':
            second = datetime.today().date()
        query = query.replace("first_term", first)
        query = query.replace("second_term", second)
        return query

    def advanced_function(term, values):
        body = extra_cases_map.get(term)
        query = body.replace("terms", ",".join(vals))
        return query

    query_map = {
        "docname": basic_function,
        "appno": basic_function,
        "scl": basic_function,
        "rulesofcourt": basic_function,
        "applicability": basic_function,
        "ecli": basic_function,
        "conclusion": basic_function,
        "resolutionnumber": basic_function,
        "separateopinions": basic_function,
        "externalsources": basic_function,
        "kpthesaurus": basic_function,
        "advopidentifier": basic_function,
        "documentcollectionid2": basic_function,
        "fulltext": full_text_function,
        "kpdate": date_function,
        "bodyprocedure": advanced_function,
        "bodyfacts": advanced_function,
        "bodycomplaints": advanced_function,
        "bodylaw": advanced_function,
        "bodyreasons": advanced_function,
        "bodyseparateopinions": advanced_function,
        "bodyappendix": advanced_function,
        "languageisocode": basic_function

    }
    start = link.index("{")
    link_dictionary = eval(link[start:])
    base_query = 'https://hudoc.echr.coe.int/app/query/results?query=contentsitename:ECHR' \
                 ' AND (NOT (doctype=PR OR doctype=HFCOMOLD OR doctype=HECOMOLD)) AND ' \
                 'inPutter&select={select}&sort=itemid%20Ascending&start={start}&length={length}'
    query_elements = list()
    if (full_text_input):
        query_elements.append(full_text_input)
    date_addition = ''
    for key in list(link_dictionary.keys()):
        if key == "kpdate":
            vals = link_dictionary.get(key)
            funct = query_map.get(key)
            date_addition = funct(key, vals)
        elif key == "sort":
            continue
        else:
            vals = link_dictionary.get(key)
            funct = query_map.get(key)
            query_elements.append(funct(key, vals))
    if date_addition:
        query_elements.append(date_addition)
    query_total = ' AND '.join(query_elements)
    final_query = base_query.replace('inPutter', query_total)

    return final_query

def determine_meta_url(link, query_payload,start_date,end_date):
    if query_payload:
        META_URL = 'http://hudoc.echr.coe.int/app/query/results' \
                   f'?query={query_payload}' \
                   '&select={select}' + \
                   '&sort=itemid Ascending' + \
                   '&start={start}&length={length}'
    elif link:
        META_URL = link_to_query(link)
    else:
        META_URL = 'http://hudoc.echr.coe.int/app/query/results' \
                   '?query=(contentsitename=ECHR) AND ' \
                   '(documentcollectionid2:"JUDGMENTS" OR ' \
                   'documentcollectionid2:"COMMUNICATEDCASES" OR ' \
                   'documentcollectionid2:"DECISIONS" OR ' \
                   'documentcollectionid2:"CLIN") AND ' \
                   'lang_inputter' \
                   '&select={select}' + \
                   '&sort=itemid Ascending' + \
                   '&start={start}&length={length}'
        if start_date and end_date:
            addition = f'(kpdate>="{start_date}" AND kpdate<="{end_date}")'
        elif start_date:
            end_date = datetime.today().date()
            addition = f'(kpdate>="{start_date}" AND kpdate<="{end_date}")'
        elif end_date:
            start_date = '1900-01-01'
            addition = f'(kpdate>="{start_date}" AND kpdate<="{end_date}")'
        else:
            addition = ''

        if addition:
            addition = " AND " + addition
            META_URL = META_URL.replace('&select', addition + '&select')
    return META_URL


def get_echr_metadata(start_id, end_id, verbose, fields, start_date, end_date, link, language, query_payload):
    """
    Read ECHR metadata into a Pandas DataFrame.
    :param int start_id: The index to start the search from.
    :param int end_id: The index to end search at, where the default fetches all results.
    :param date start_date: The point from which to save cases.
    :param date end_date: The point before which to save cases.
    :param bool verbose: Whether or not to print extra information.
    """
    data = []
    if not fields:
        fields = ['itemid', 'applicability', 'appno', 'article', 'conclusion', 'docname',
                  'doctype', 'doctypebranch', 'ecli', 'importance', 'judgementdate',
                  'languageisocode', 'originatingbody', 'violation', 'nonviolation',
                  'extractedappno', 'scl', 'publishedby', 'representedby', 'respondent',
                  'separateopinion', 'sharepointid', 'externalsources', 'issue', 'referencedate',
                  'rulesofcourt', 'DocId', 'WorkId', 'Rank', 'Author', 'Size', 'Path',
                  'Description', 'Write', 'CollapsingStatus', 'HighlightedSummary',
                  'HighlightedProperties', 'contentclass', 'PictureThumbnailURL',
                  'ServerRedirectedURL', 'ServerRedirectedEmbedURL', 'ServerRedirectedPreviewURL',
                  'FileExtension', 'ContentTypeId', 'ParentLink', 'ViewsLifeTime', 'ViewsRecent',
                  'SectionNames', 'SectionIndexes', 'SiteLogo', 'SiteDescription', 'deeplinks',
                  'SiteName', 'IsDocument', 'LastModifiedTime', 'FileType', 'IsContainer',
                  'WebTemplate', 'SecondaryFileExtension', 'docaclmeta', 'OriginalPath',
                  'EditorOWSUSER', 'DisplayAuthor', 'ResultTypeIdList', 'PartitionId', 'UrlZone',
                  'AAMEnabledManagedProperties', 'ResultTypeId', 'rendertemplateid']

    META_URL = determine_meta_url(link,query_payload,start_date,end_date)
        # An example url: "https://hudoc.echr.coe.int/app/query/results?query=(contentsitename=ECHR)%20AND%20(documentcollectionid2:%22JUDGMENTS%22%20OR%20documentcollectionid2:%22COMMUNICATEDCASES%22%20OR%20documentcollectionid2:%22DECISIONS%22%20OR%20documentcollectionid2:%22CLIN%22)&select=itemid,applicability,application,appno,article,conclusion,decisiondate,docname,documentcollectionid,%20documentcollectionid2,doctype,doctypebranch,ecli,externalsources,extractedappno,importance,introductiondate,%20isplaceholder,issue,judgementdate,kpdate,kpdateAsText,kpthesaurus,languageisocode,meetingnumber,%20originatingbody,publishedby,Rank,referencedate,reportdate,representedby,resolutiondate,%20resolutionnumber,respondent,respondentOrderEng,rulesofcourt,separateopinion,scl,sharepointid,typedescription,%20nonviolation,violation&sort=itemid%20Ascending&start=0&length=200"



    META_URL = META_URL.replace(' ', '%20')
    META_URL = META_URL.replace('"', '%22')
    META_URL = META_URL.replace('%5C','')

    language_input = basic_function('languageisocode', language)
    if not link:
        META_URL = META_URL.replace('lang_inputter', language_input)

    META_URL = META_URL.replace('{select}', ','.join(fields))

    url = META_URL.format(start=0, length=1)
    logging.info(url)
    r = requests.get(url)
    resultcount = r.json()['resultcount']
    logging.info("available results: " + str(resultcount))

    if not end_id:
        end_id = resultcount
    if verbose:
        logging.info(f'Fetching {end_id - start_id} results from index {start_id} to index {end_id} ' +
                     f'{f" and filtering cases after {start_date}" if start_date and not link and not query_payload else ""} {f"and filtering cases before {end_date}" if end_date and not link and not query_payload else "."}')

    timeout = 60
    retry = 3
    if start_id + end_id > 500:  # HUDOC does not let you fetch more than 500 items in one go.
        for i in range(start_id, end_id, 500):
            if verbose:
                logging.info(" - Fetching information from cases {} to {}.".format(i, i + 500))
            # Format URL based on the incremented index.
            url = META_URL.format(start=i, length=500)
            if verbose:
                logging.info(url)

            # Get the response.
            r = get_r(url, timeout, retry, verbose)
            if r is not None:
                # Get the results list
                temp_dict = r.json()['results']
                # Get every document from the results list.
                for result in temp_dict:
                    data.append(result['columns'])

    else:
        # Format URL based on start and length
        url = META_URL.format(start=start_id, length=end_id)
        if verbose:
            logging.info(url)

        r = get_r(url, timeout, retry, verbose)
        if r is not None:
            # Get the results list
            temp_dict = r.json()['results']
            # Get every document from the results list.
            for result in temp_dict:
                data.append(result['columns'])

    if len(data) == 0:
        logging.info("Search results ended up empty")
        return False
    return pd.DataFrame.from_records(data)
