import requests
import pandas as pd


# TODO find a better way to do this.....
class ContinueException(Exception): pass


def r_get_timeout(url, timeout, retry, verbose):
    returned = False
    count = 0

    while not returned:
        try:
            r = requests.get(url, timeout=timeout)
            returned = True
        except requests.exceptions.ReadTimeout:
            count += 1
            if verbose:
                print(f'Timeout!! Retry {count}...')
            if count > retry:
                raise ContinueException()
            else:
                pass

    return r



def read_echr_metadata(start_id=0, end_id=None, fields=None, verbose=True):
    """
    Read ECHR metadata into a Pandas DataFrame.
    :param start_id: result index to start search from
    :param end_id: result index to end search at (default None fetches all results)
    :param fields: list of meta attribute names to return (default None fetches all attributes)
    :param verbose: bool whether or not to print fetched URLs
    :return:
    """

    data = []
    fields = ['itemid', 'appno', 'article', 'conclusion', 'docname', 'doctype', 'doctypebranch', 'ecli', 'importance',
              'judgmentdate', 'languageisocode', 'originatingbody', 'publishedby', 'extractedappno']
    META_URL = 'http://hudoc.echr.coe.int/app/query/results' \
               '?query=(contentsitename=ECHR) AND ' \
               '(documentcollectionid2:"JUDGMENTS" OR documentcollectionid2:"COMMUNICATEDCASES") AND' \
               '(languageisocode:"ENG")' \
               '&select={select}' + \
               '&sort=itemid Ascending' + \
               '&start={start}&length={length}'

    META_URL = META_URL.replace(' ', '%20')
    META_URL = META_URL.replace('"', '%22')
    # example url: "https://hudoc.echr.coe.int/app/query/results?query=(contentsitename=ECHR)%20AND%20(documentcollectionid2:%22JUDGMENTS%22%20OR%20documentcollectionid2:%22COMMUNICATEDCASES%22)&select=itemid,applicability,application,appno,article,conclusion,decisiondate,docname,documentcollectionid,%20documentcollectionid2,doctype,doctypebranch,ecli,externalsources,extractedappno,importance,introductiondate,%20isplaceholder,issue,judgementdate,kpdate,kpdateAsText,kpthesaurus,languageisocode,meetingnumber,%20originatingbody,publishedby,Rank,referencedate,reportdate,representedby,resolutiondate,%20resolutionnumber,respondent,respondentOrderEng,rulesofcourt,separateopinion,scl,sharepointid,typedescription,%20nonviolation,violation&sort=itemid%20Ascending&start=0&length=2"

    # get total number of results:
    url = META_URL.format(select=','.join(fields), start=0, length=2)
    r = requests.get(url)
    resultcount = r.json()['resultcount']

    print("available results: ", resultcount)

    if not end_id:
        end_id = resultcount
    end_id = start_id + end_id

    if start_id + end_id > 500:  # HUDOC does not allow fetching more than 500 items at the same time
        for i in range(start_id, end_id, 500):
            print(" - Fetching information from cases {} to {}.".format(i, i + 500))

            # Fromat URL based on the incremented index
            url = META_URL.format(select=','.join(fields), start=i, length=500)
            if verbose:
                print(url)
            r = requests.get(url)

            # try:
            #    r_get_timeout(url=url, timeout=10, retry=3, verbose=verbose)
            # except ContinueException:
            #    continue

            # try:
            #     r = requests.get(url, timeout=10)
            # except requests.exceptions.ReadTimeout:
            #     if verbose:
            #         print('Timeout... Retry')
            #     r = requests.get(url, timeout=10)

            # Get the results list
            temp_dict = r.json()['results']

            # Get every doc from the results list
            for result in temp_dict:
                data.append(result['columns'])
    else:
        # Format URL based on start and length
        url = META_URL.format(select=','.join(
            fields), start=start_id, length=end_id)
        if verbose:
            print(url)
        r = requests.get(url)

        # Get the results list
        temp_dict = r.json()['results']

        # Get every doc from the results list
        for result in temp_dict:
            data.append(result['columns'])

    return pd.DataFrame.from_records(data), resultcount
