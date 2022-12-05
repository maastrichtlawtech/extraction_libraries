from echr_extractor.ECHR_metadata_harvester import read_echr_metadata
from echr_extractor.ECHR_html_downloader import download_full_text_main
from pathlib import Path
import os
import json

def get_echr(start_id=None,end_id=None,count=None, save_file='y'):
    if not start_id:
        start_id=0
    if count:
        end_id=int(start_id)+count
    if end_id:
        filename=f"echr_metadata_{start_id}-{end_id}"
    else:
        filename = f"echr_metadata_{start_id}-ALL"
    print("--- STARTING ECHR DOWNLOAD ---")
    df, resultcount = read_echr_metadata(end_id=end_id,start_id=start_id,verbose=False)
    if df is False and resultcount is False:
        return False
    print("\n--- DONE ---")
    if save_file == "y":
        # saving file
        Path('data').mkdir(parents=True, exist_ok=True)
        file_path = os.path.join('data', filename + '.csv')
        df.to_csv( file_path,index=False)
        return df
    else:
        return df


def get_echr_extra(start_id=None,end_id=None,count=None, save_file='y',threads=10):
    if not start_id:
        start_id = 0
    if count:
        end_id = int(start_id) + count
    if end_id:
        filename = f"echr_metadata_{start_id}-{end_id}"
    else:
        filename = f"echr_metadata_{start_id}-ALL"
    df = get_echr(start_id=start_id,end_id=end_id,count=count, save_file='n')
    if df is False:
        return False,False
    json_list = download_full_text_main(df,threads)
    if save_file == "y":
        filename_json = filename.replace("metadata","full_text")
        Path('data').mkdir(parents=True, exist_ok=True)
        file_path = os.path.join('data', filename + '.csv')
        df.to_csv(file_path, index=False)
        file_path_json = os.path.join('data', filename_json + '.json')
        with open(file_path_json, "w") as f:
            json.dump(json_list, f)
        return df,json_list
    else:
        return df,json_list

