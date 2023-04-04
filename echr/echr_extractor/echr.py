from echr_extractor.ECHR_metadata_harvester import read_echr_metadata
from echr_extractor.ECHR_html_downloader import download_full_text_main
from echr_extractor.ECHR_nodes_edges_list_transform import echr_nodes_edges
from pathlib import Path
import pandas as pd
import os
import json

"""
I have replaced the function definition to take all arguments n eede to call read_echr_metadata and I have also
replaced the file naming lines. The old code is commented out I didn't delete anything. :)
On top of this the lines which deal with defining default values have been commented out because this is
handled in read_echr_metadata. It can also be done here but then it should be removed from the other method. 
It will probably be necissary to add some file handling to prevent overwriting. I'm not sure if you have plans for this
already but feel free to shoot me a message about it seeing as I did something similar for the ECHR branch. @Benjamin
"""


def get_echr(start_id=0, end_id=None, start_date=None, count=None, end_date=None, verbose=False, save_file='y',
             fields=None,link=None, language=["FRE"]):
    df = pd.DataFrame()
    resultcount = 0
    if count:
        end_id = int(start_id) + count
    for lang in language:

        print(f"--- STARTING ECHR DOWNLOAD FOR {lang} ---")
        #fields = None
        # append the dataframes from each language to the same dataframe if df is not False
        if df is not False and resultcount is not False:
            df = df.append(read_echr_metadata(start_id=start_id, end_id=end_id, start_date=start_date, end_date=end_date,
                                             verbose=verbose, fields=fields,link=link, language=lang)[0])
            resultcount += read_echr_metadata(start_id=start_id, end_id=end_id, start_date=start_date, end_date=end_date,
                                                verbose=verbose, fields=fields,link=link, language=lang)[1]
        elif df is False and resultcount is False:
            continue
    if df is False and resultcount is False:
        return False
    if save_file == "y":
        filename = determine_filename(start_id, end_id, start_date, end_date)
        Path('data').mkdir(parents=True, exist_ok=True)
        file_path = os.path.join('data', filename + '.csv')
        df.to_csv(file_path, index=False)
        print("\n--- DONE ---")
        return df
    else:
        print("\n--- DONE ---")
        return df


def determine_filename(start_id, end_id, start_date, end_date):
    if end_id:
        if start_date and end_date:
            filename = f"echr_metadata_index_{start_id}-{end_id}_dates_{start_date}-{end_date}"
        elif start_date:
            filename = f"echr_metadata_{start_id}-{end_id}_dates_{start_date}-END"
        elif end_date:
            filename = f"echr_metadata_{start_id}-{end_id}_datesSTART-{end_date}"
        else:
            filename = f"echr_metadata_{start_id}-{end_id}_dates_START-END"
    else:
        if start_date and end_date:
            filename = f"echr_metadata_index_{start_id}-ALL_dates_{start_date}-{end_date}"
        elif start_date:
            filename = f"echr_metadata_{start_id}-ALL_dates_{start_date}-END"
        elif end_date:
            filename = f"echr_metadata_{start_id}-ALL_dates_START-{end_date}"
        else:
            filename = f"echr_metadata_{start_id}-ALL_dates_START-END"
    return filename


def get_echr_extra(start_id=0, end_id=None, start_date=None, count=None, end_date=None, verbose=False,
                    save_file='y', threads=10,fields=None,link=None, language=["ENG"]):
    if count:
        end_id = int(start_id) + count
    df = get_echr(start_id=start_id, end_id=end_id, start_date=start_date, end_date=end_date, verbose=verbose,
                   count=count, save_file='n',fields=fields,link=link, language=language)
    print("Full-text download will now begin")
    if df is False:
        return False, False
    json_list = download_full_text_main(df, threads)
    print("Full-text download finished")
    if save_file == "y":
        filename = determine_filename(start_id, end_id, start_date, end_date)
        filename_json = filename.replace("metadata", "full_text")
        Path('data').mkdir(parents=True, exist_ok=True)
        file_path = os.path.join('data', filename + '.csv')
        df.to_csv(file_path, index=False)
        file_path_json = os.path.join('data', filename_json + '.json')
        with open(file_path_json, "w") as f:
            json.dump(json_list, f)
        return df, json_list
    else:
        return df, json_list

def get_nodes_edges(metadata_path, save_file='y'):


    nodes, edges = echr_nodes_edges(metadata_path)
    if save_file == "y":
        Path('data').mkdir(parents=True, exist_ok=True)
        edges.to_csv(os.path.join('data', 'ECHR_edges.csv'), index=False, encoding='utf-8')
        nodes.to_json(os.path.join('data', 'ECHR_nodes.json'), orient="records")
        edges.to_json(os.path.join('data', 'ECHR_edges.json'), orient="records")
        return nodes, edges

    return nodes, edges


