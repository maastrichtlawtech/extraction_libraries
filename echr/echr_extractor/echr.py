from echr_extractor.ECHR_metadata_harvester import read_echr_metadata
from echr_extractor.ECHR_html_downloader import download_full_text_main
from pathlib import Path
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
             fields=None):
    if count:
        end_id = int(start_id) + count
    print("--- STARTING ECHR DOWNLOAD ---")
    #fields = None
    df, resultcount = read_echr_metadata(start_id=start_id, end_id=end_id, start_date=start_date, end_date=end_date,
                                         verbose=verbose, fields=fields)
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


def get_echr_extra(start_id=0, end_id=None, start_date=None, count=None, end_date=None, verbose=True,
                   skip_missing_dates=True, save_file='y', threads=10,fields=None):
    if count:
        end_id = int(start_id) + count
    df = get_echr(start_id=start_id, end_id=end_id, start_date=start_date, end_date=end_date, verbose=verbose,
                  skip_missing_dates=skip_missing_dates, count=count, save_file='n',fields=fields)
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


