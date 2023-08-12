import re
import dateparser
import numpy as np
import pandas as pd
from tqdm import tqdm
from echr_extractor.clean_ref import clean_pattern


def open_metadata(PATH_metadata):
    """
    Finds the ECHR metadata file and loads it into a dataframe
    
    param filename_metadata: string with path to metadata
    """
    try:
        df = pd.read_csv(PATH_metadata)  # change hard coded path
        return df
    except FileNotFoundError:
        print("File not found. Please check the path to the metadata file.")
        return False


def concat_metadata(df):
    agg_func = {'itemid': 'first', 'appno': 'first', 'article': 'first', 'conclusion': 'first', 'docname': 'first',
                'doctype': 'first',
                'doctypebranch': 'first', 'ecli': 'first', 'importance': 'first', 'judgementdate': 'first',
                'languageisocode': ', '.join, 'originatingbody': 'first',
                'violation': 'first', 'nonviolation': 'first', 'extractedappno': 'first', 'scl': 'first'}
    new_df = df.groupby('ecli').agg(agg_func)
    # print(new_df)
    return new_df


def get_language_from_metadata(df):
    df = concat_metadata(df)
    df.to_json('langisocode-nodes.json', orient="records")


def retrieve_edges_list(df):
    """
    Returns a dataframe consisting of 2 columns 'source' and 'target' which
    indicate a reference link between cases.

    params:
    df -- the node list extracted from the metadata
    df -- the complete dataframe from the metadata
    """
    edges = list()

    count = 0
    missing_cases = []
    bar = tqdm(total=len(df.index), colour="GREEN", position=0, leave=True)
    for index, item in df.iterrows():
        bar.update(1)
        eclis = []
        extracted_appnos = []
        if item.extractedappno is not np.nan:
            extracted_appnos = item.extractedappno.split(';')
        if item.scl is np.nan:
            continue
        """
            Split the references from the scl column i nto a list of references.

            Example:
            references in string: "Ali v. Switzerland, 5 August 1998, § 32, Reports of Judgments and 
            Decisions 1998-V;Sevgi Erdogan v. Turkey (striking out), no. 28492/95, 29 April 2003"

            ["Ali v. Switzerland, 5 August 1998, § 32, Reports of Judgments and 
            Decisions 1998-V", "Sevgi Erdogan v. Turkey (striking out), no. 
            28492/95, 29 April 2003"]
            """
        ref_list = item.scl.split(';')
        new_ref_list = [i.replace('\n', '') for i in ref_list]

        for ref in new_ref_list:
            app_number = re.findall("\d{3,5}/\d{2}", ref)

            app_number.extend(extracted_appnos)

            app_number = set(app_number)

            if len(app_number) > 0:
                # get dataframe with all possible cases by application number
                app_number = [';'.join(app_number)]
                case = lookup_app_number(app_number, df)
                if len(case) == 0:  # if failed try name?
                    case = lookup_casename(ref, df)
            else:  # if no application number in reference
                # get dataframe with all possible cases by casename
                case = lookup_casename(ref, df)

            components = ref.split(',')
            # get the year of case
            year_from_ref = get_year_from_ref(components)

            # remove cases in different language than reference
            case = remove_cases_based_on_language(case, components)
            case = remove_cases_based_on_year(case, year_from_ref)

            if len(case) > 0:
                for _, row in case.iterrows():
                    eclis.append(row.ecli)
            else:
                count = count + 1
                missing_cases.append(ref)

        eclis = set(eclis)

        # add ecli to edges list
        if len(eclis) == 0:  # This should not have to happen at every iteration, concat might be slow
            continue
        for target in eclis:
            edges.append({'source': item.ecli, 'target': target})

    edges = pd.DataFrame.from_records(edges)
    return edges


def remove_cases_based_on_year(case, year_from_ref):
    for id, i in case.iterrows():
        if i.judgementdate is np.nan:
            continue
        try:
            date = dateparser.parse(i.judgementdate)
        except:
            date = False
        if date:
            year_from_case = date.year
            if year_from_case - year_from_ref == 0:
                case = case[
                    case['judgementdate'].str.contains(str(year_from_ref), regex=False,
                                                       flags=re.IGNORECASE, na=False)]
    return case


def remove_cases_based_on_language(cases, components):
    for id, it in cases.iterrows():
        if 'v.' in components[0]:
            lang = 'ENG'
        else:
            lang = 'FRE'

        if lang not in it.languageisocode:
            cases = cases[cases['languageisocode'].str.contains(lang, regex=False, flags=re.IGNORECASE, na=False)]
    return cases


def lookup_app_number(pattern, df):
    """
    Returns a list with rows containing the cases linked to the found app numbers.
    """
    row = df.loc[df['appno'].isin(pattern)]

    if row.empty:
        return pd.DataFrame()
    elif row.shape[0] > 1:
        return row
    else:
        return row


def lookup_casename(ref, df):
    """
    Process the reference for lookup in metadata.
    Returns the rows corresponding to the cases.

    - Example of the processing (2 variants) -

    Original reference from scl:
    - Hentrich v. France, 22 September 1994, § 42, Series A no. 296-A
    - Eur. Court H.R. James and Others judgment of 21 February 1986,
    Series A no. 98, p. 46, para. 81

    Split on ',' and take first item:
    Hentrich v. France
    Eur. Court H.R. James and Others judgment of 21 February 1986

    If certain pattern from CLEAN_REF in case name, then remove:
    Eur. Court H.R. James and Others judgment of 21 February 1986 -->
        James and Others

    Change name to upper case and add additional text to match metadata:
    Hentrich v. France --> CASE OF HENTRICH V. FRANCE
    James and Others --> CASE OF JAMES AND OTHERS
    """
    name = get_casename(ref)

    # DEV note: In case, add more patterns to clean_ref.py in future
    patterns = clean_pattern

    uptext = name.upper()

    if 'NO.' in uptext:
        uptext = uptext.replace('NO.', 'No.')

    if 'BV' in uptext:
        uptext = uptext.replace('BV', 'B.V.')

    if 'V.' in name:
        uptext = uptext.replace('V.', 'v.')
        lang = 'ENG'
    else:
        uptext = uptext.replace('C.', 'c.')
        lang = 'FRE'

    for pattern in patterns:
        uptext = re.sub(pattern, '', uptext)

    uptext = re.sub(r'\[.*', "", uptext)
    uptext = uptext.strip()
    row = df[df['docname'].str.contains(uptext, regex=False, flags=re.IGNORECASE)]

    # if len(row) == 0:
    #     print("no cases matched: ", name)

    return row


def get_casename(ref):
    count = 0
    if 'v.' in ref:
        slice_at_versus = ref.split('v.')  # skip if typo (count how many)
    elif 'c.' in ref:
        slice_at_versus = ref.split('c.')
    else:
        count = count + 1
        name = ref.split(',')
        return name[0]

    num_commas = slice_at_versus[0].count(',')

    if num_commas > 0:
        num_commas = num_commas + 1
        name = ",".join(ref.split(",", num_commas)[:num_commas])
    else:
        name = ref.split(',')
        return name[0]
    return name


def get_year_from_ref(ref):
    for component in ref:
        if '§' in component:
            continue
        component = re.sub('judgment of ', "", component)
        if dateparser.parse(component) is not None:
            date = dateparser.parse(component)
        elif ("ECHR" in component or "CEDH" in component):
            if ("ECHR" in component or "CEDH" in component):
                date = re.sub('ECHR ', '', component)
                date = re.sub('CEDH ', '', date)
                date = date.strip()
                date = re.sub('-.*', '', date)
                date = re.sub('\s.*', '', date)
                date = dateparser.parse(date)

    try:
        return date.year
    except:
        return 0


def echr_nodes_edges(metadata_path=None, data=None):
    """
    Create nodes and edges list for the ECHR data.
    """
    print('\n--- COLLECTING METADATA ---\n')
    if metadata_path:
        data = open_metadata(metadata_path)
    elif data is None:
        print("No dataframe data provided. Returning...")
        return "", ""
    print('\n--- EXTRACTING NODES LIST ---\n')
    # get_language_from_metadata(nodes)

    print('\n--- EXTRACTING EDGES LIST ---\n')
    edges = retrieve_edges_list(data)

    # nodes.to_json(JSON_ECHR_NODES, orient="records")
    # edges.to_json(JSON_ECHR_EDGES, orient="records")
    return data, edges
