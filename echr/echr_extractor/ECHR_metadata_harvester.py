import requests
import dateutil.parser
from datetime import datetime

import pandas as pd


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
                print(f"Timeout. Retry attempt {count}.")
            if count > retry:
                if verbose:
                    print(f"Unable to connect to {url}. Skipping this batch.")
                return None
    return None


def read_echr_metadata(start_id, end_id, start_date, end_date, verbose, skip_missing_dates, fields):
    """
    Read ECHR metadata into a Pandas DataFrame.
    :param int start_id: The index to start the search from.
    :param int end_id: The index to end search at, where the default fetches all results.
    :param date start_date: The point from which to save cases.
    :param date end_date: The point before which to save cases.
    :param bool verbose: Whther or not to print extra information.
    :param bool skip_missing_dates: Whether or not to save cases with missing dates.
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
    META_URL = 'http://hudoc.echr.coe.int/app/query/results' \
               '?query=(contentsitename=ECHR) AND ' \
               '(documentcollectionid2:"JUDGMENTS" OR \
                 documentcollectionid2:"COMMUNICATEDCASES" OR \
                 documentcollectionid2:"DECISIONS" OR \
                 documentcollectionid2:"CLIN") AND ' \
               '(languageisocode:"ENG")' \
               '&select={select}' + \
               '&sort=itemid Ascending' + \
               '&start={start}&length={length}'

    META_URL = META_URL.replace(' ', '%20')
    META_URL = META_URL.replace('"', '%22')
    # An example url: "https://hudoc.echr.coe.int/app/query/results?query=(contentsitename=ECHR)%20AND%20(documentcollectionid2:%22JUDGMENTS%22%20OR%20documentcollectionid2:%22COMMUNICATEDCASES%22%20OR%20documentcollectionid2:%22DECISIONS%22%20OR%20documentcollectionid2:%22CLIN%22)&select=itemid,applicability,application,appno,article,conclusion,decisiondate,docname,documentcollectionid,%20documentcollectionid2,doctype,doctypebranch,ecli,externalsources,extractedappno,importance,introductiondate,%20isplaceholder,issue,judgementdate,kpdate,kpdateAsText,kpthesaurus,languageisocode,meetingnumber,%20originatingbody,publishedby,Rank,referencedate,reportdate,representedby,resolutiondate,%20resolutionnumber,respondent,respondentOrderEng,rulesofcourt,separateopinion,scl,sharepointid,typedescription,%20nonviolation,violation&sort=itemid%20Ascending&start=0&length=200".

    # get total number of results:
    url = META_URL.format(select=','.join(fields), start=0, length=1)
    r = requests.get(url)
    resultcount = r.json()['resultcount']
    print("available results: ", resultcount)

    if not end_id:
        end_id = resultcount
    if not start_date:
        start_date = dateutil.parser.parse("01-01-1000", dayfirst=True).date()
    else:
        start_date = dateutil.parser.parse(start_date).date()
    if not end_date:
        end_date = datetime.now().date()
    else:
        end_date = dateutil.parser.parse(end_date).date()
    if verbose:
        print(f'Fetching {end_id - start_id} results from index {start_id} to index {end_id} and \
              filtering for cases after {start_date} and before {end_date}.')

    timeout = 6
    retry = 3
    if start_id + end_id > 500:  # HUDOC does not let you fetch more than 500 items in one go.
        for i in range(start_id, end_id, 500):
            if verbose:
                print(" - Fetching information from cases {} to {}.".format(i, i + 500))
            # Format URL based on the incremented index.
            url = META_URL.format(select=','.join(fields), start=i, length=500)
            if verbose:
                print(url)

            # Get the response.
            r = get_r(url, timeout, retry, verbose)
            if r is not None:
                # Get the results list
                temp_dict = r.json()['results']
                # Get every document from the results list.
                for result in temp_dict:
                    try:
                        case_date = dateutil.parser.parse(result['columns']['judgementdate'], dayfirst=True).date()
                        if start_date <= case_date <= end_date:
                            data.append(result['columns'])
                    except dateutil.parser.ParserError:
                        if not skip_missing_dates:
                            data.append(result['columns'])
    else:
        # Format URL based on start and length
        url = META_URL.format(select=','.join(fields), start=start_id, length=end_id)
        if verbose:
            print(url)

        r = get_r(url, timeout, retry, verbose)
        if r is not None:
            # Get the results list
            temp_dict = r.json()['results']
            # Get every document from the results list.
            for result in temp_dict:
                try:
                    case_date = dateutil.parser.parse(result['columns']['judgementdate']).date()
                    if start_date <= case_date <= end_date:
                        data.append(result['columns'])
                except dateutil.parser.ParserError:
                    if not skip_missing_dates:
                        data.append(result['columns'])

    if len(data) == 0:
        print("Search results ended up empty")
        return False, False
    return pd.DataFrame.from_records(data), resultcount
