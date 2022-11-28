import sys
import threading
import time
from io import StringIO
from os.path import dirname, abspath
import pandas as pd
from cellar_extractor.sparql import get_citations_csv, get_cited, get_citing, run_eurlex_webservice_query
from cellar_extractor.eurlex_scraping import extract_dictionary_from_webservice_query

sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))

"""
Method used by separate threads for the multi-threading method of adding citations to the dataframe
Sends a query which returns a csv file containing the the celex identifiers of cited works for each case.
Works with multi-case queries, at_once is the variable deciding for how many cases are used with each query.
"""


def execute_citations(csv_list, citations):
    at_once = 1000
    for i in range(0, len(citations), at_once):
        new_csv = get_citations_csv(citations[i:(i + at_once)])
        csv_list.append(StringIO(new_csv))


"""
This method replaces replaces the column with citations.

Old column -> links to cited works
New column -> celex identifiers of cited works

It uses multithreading, which is very much recommended.
Uses a query to get the citations in a csv format from the endpoint. * 

* More details in the query method.
"""


def add_citations(data, threads):
    name = "WORK CITES WORK. CI / CJ"
    celex = data.loc[:, "CELEX IDENTIFIER"]

    length = celex.size
    if length > 100:  # to avoid getting problems with small files
        at_once_threads = int(length / threads)
    else:
        at_once_threads = length
    all_csv = list()
    threads = []
    for i in range(0, length, at_once_threads):
        curr_celex = celex[i:(i + at_once_threads)]
        t = threading.Thread(target=execute_citations, args=(all_csv, curr_celex))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    df = pd.concat(map(pd.read_csv, all_csv), ignore_index=True)
    celexes = pd.unique(df.loc[:, 'celex'])
    citations = pd.Series([], dtype='string')
    for celex in celexes:
        index = data[data['CELEX IDENTIFIER'] == celex].index.values
        cited = df[df['celex'] == celex].loc[:, "citedD"]
        string = ";".join(cited)
        citations[index[0]] = string
    data.pop(name)
    citations.sort_index(inplace=True)
    data.insert(1, name, citations)


"""
Method used by separate threads for the multi-threading method of adding citations to the dataframe
Sends a query which returns a csv file containing the the celex identifiers of cited works for each case.
Works with multi-case queries, at_once is the variable deciding for how many cases are used with each query.
"""


def execute_citations_separate(cited_list, citing_list, citations):
    at_once = 1000
    for i in range(0, len(citations), at_once):
        new_cited = get_cited(citations[i:(i + at_once)], 1)
        new_citing = get_citing(citations[i:(i + at_once)], 1)
        cited_list.append(StringIO(new_cited))
        citing_list.append(StringIO(new_citing))


"""

Method used by separate threads for the multi-threading method of adding citations to the dataframe
Uses the eurlex webservices.
Also used for the single-thread approach.

"""


def execute_citations_webservice(dictionary_list, celexes, username, password):
    at_once = 100
    success=0
    retry=0
    base_query = "SELECT DN,CI WHERE DN = %s"
    base_contains_query = "SELECT DN,CI WHERE DN ~ %s"
    for i in range(0, len(celexes), at_once):
        curr_celex = celexes[i:(i + at_once)]
        normal_list, contains_list = clean_celex(curr_celex)
        input=" OR ".join(normal_list)
        normal_query = base_query % (str(input))
        failure = False
        if len(normal_list) == 0:
            failure=True
        while not failure:
            response = run_eurlex_webservice_query(normal_query, username, password)
            if response.status_code == 500:
                perc=i*100/len(celexes)
                print(f"Limit of web service usage reached! Citations collection will stop here at {perc} % of citations downloaded."
                      f"\nThere were {success} successful queries and {retry} retries")
                return
            try:
                dictionary = extract_dictionary_from_webservice_query(response)
                dictionary_list.append(dictionary)
                success+=1
                failure = True
            except:
                retry+=1
                print(response.content)
                time.sleep(0.5)
        if len(contains_list) > 0:
            failure = False
            input=" OR ".join(contains_list)
            contains_query = base_contains_query % (str(input))
            while not failure:
                contains_response = run_eurlex_webservice_query(contains_query, username, password)
                if contains_response.status_code == 500:
                    perc = i * 100 / len(celexes)
                    print(
                        f"Limit of web service usage reached! Citations collection will stop here at {perc} % of citations downloaded."
                        f"\nThere were {success} successful queries and {retry} retries")
                    return
                try:
                    dictionary = extract_dictionary_from_webservice_query(contains_response)
                    dictionary_list.append(dictionary)
                    success+=1
                    failure = True
                except:
                    retry+=1
                    print(response.content)
                    time.sleep(0.5)


"""

Method used to separate celex id's when there are multiple pointing to the same document.
On top of that, separates celex id's with '(' and ')', these brackets are keywords for the webservice query.
After separated, a different query is ran for the normal celexes, and those with brackets.

"""


def clean_celex(celex):
    normal_list = list()
    contains_list = list()
    for c1 in celex:
        if ";" in c1:
            celexes = c1.split(";")
            for c2 in celexes:
                if "_" not in c2:
                    if "(" in c2:
                        contains_list.append(c2.replace("(", "").replace(")", ""))
                    else:
                        normal_list.append(c2)
        else:
            if "(" in c1:
                contains_list.append(c1.replace("(", "").replace(")", ""))
            else:
                normal_list.append(c1)
    return normal_list, contains_list


"""

Method used for creation of a dictionary of documents citing the document.
Uses the dictionary of documents cited by the document.
Output will more than likely be bigger than the input dictionary, as it will also include treaties and other documents,
which are not being extracted by the cellar extractor.

"""
def allowed_id(id):
    if id != "":
        return id[0] == 8 or id[0] == 6
    else:
        return False

def reverse_citing_dict(citing):
    cited = dict()
    for k in citing:
        citeds = citing.get(k).split(";")
        for c in citeds:
            if allowed_id(c):
                if c in cited:
                    cited[c] = cited.get(c) + "," + k
                else:
                    cited[c] = k
    return cited


"""

Method used to add the dictionaries to the dataframe.
Used by the citations adding from the eurlex webservices.
Implements checks, for whether the document whose data we want to add exists in the original dataframe.

"""


def add_dictionary_to_df(df, dictionary, column_title):
    column = pd.Series([], dtype='string')
    celex = df.loc[:, "CELEX IDENTIFIER"]
    for k in dictionary:
        if celex.str.contains(k).any():
            index = df.index[df["CELEX IDENTIFIER"].str.contains(k)].tolist()
            column[index[0]] = dictionary.get(k)
    column.sort_index(inplace=True)
    df.insert(1, column_title, column)


"""
Main method for citations adding via eurlex webservices.

Old column -> links to cited works
New columns -> celex identifiers of cited works and works citing current work

"""


def add_citations_separate_webservice(data, username, password):
    celex = data.loc[:, "CELEX IDENTIFIER"]
    query = " SELECT CI, DN WHERE DN = 62019CJ0668"
    response = run_eurlex_webservice_query(query, username, password)
    if response.status_code == 500 :
        if "WS_MAXIMUM_NB_OF_WS_CALLS" in response.text:
            print("Maximum number of calls to the eurlex webservices reached! The code will skip the citations download.")
            return
        else:
            print("Incorrect username and password for eurlex webservices! (The account login credentials and webservice) "
              "login credentials are different)")
            sys.exit(2)
    elif response.status_code == 403:
        print("Webservice connection was blocked, eurlex might be going through maintenance right now.")
        sys.exit(2)
    else:
        print("Webservice connection was successful!")
    dictionary_list = list()
    execute_citations_webservice(dictionary_list,celex,username,password)
    citing_dict = dict()
    for d in dictionary_list:
        citing_dict.update(d)
    print("Webservice extraction finished, adding to dataframe.")
    time.sleep(1) # It seemed to print out the length of dictionary wrong, even when it was equal to 1000.
    cited_dict = reverse_citing_dict(citing_dict)

    add_dictionary_to_df(data, citing_dict, "citing")
    add_dictionary_to_df(data, cited_dict, "cited_by")


"""
This method replaces replaces the column with citations.

Old column -> links to cited works
New column -> celex identifiers of cited works

It uses multithreading, which is very much recommended.
Uses a query to get the citations in a csv format from the endpoint. * 

* More details in the query method.
"""


def add_citations_separate(data, threads):
    celex = data.loc[:, "CELEX IDENTIFIER"]
    length = celex.size
    if length > 100:  # to avoid getting problems with small files
        at_once_threads = int(length / threads)
    else:
        at_once_threads = length
    cited_csv = list()
    citing_csv = list()
    threads = []

    for i in range(0, length, at_once_threads):
        curr_celex = celex[i:(i + at_once_threads)]
        t = threading.Thread(target=execute_citations_separate, args=(cited_csv, citing_csv, curr_celex))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    cited = pd.concat(map(pd.read_csv, cited_csv), ignore_index=True)
    citing = pd.concat(map(pd.read_csv, citing_csv), ignore_index=True)

    celexes = pd.unique(cited.loc[:, 'celex'])

    citing_df = pd.Series([], dtype='string')
    cited_df = pd.Series([], dtype='string')
    for cel in celexes:
        index = data[data['CELEX IDENTIFIER'] == cel].index.values

        cited_data = cited[cited['celex'] == celex].loc[:, "citedD"]
        citing_data = citing[citing['celex'] == celex].loc[:, "citedD"]

        string_cited = ";".join(cited_data)
        string_citing = ";".join(citing_data)

        citing_df[index[0]] = string_citing
        cited_df[index[0]] = string_cited

    citing_df.sort_index(inplace=True)
    cited_df.sort_index(inplace=True)

    data.insert(1, "citing", citing_df)
    data.insert(1, "cited_by", cited_df)


if __name__ == '__main__':
    B = 2
