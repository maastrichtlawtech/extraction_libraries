#from echr_extractor.ECHR_metadata_harvester import read_echr_metadata
from ECHR_metadata_harvester import read_echr_metadata
#from echr_extractor.ECHR_html_downloader import download_full_text_main
from ECHR_html_downloader import download_full_text_main
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

#def get_echr(start_id=None, end_id=None, count=None, save_file='y'):
def get_echr(start_id=0, end_id=None, start_date=None, end_date=None, verbose=True, skip_missing_dates=True, save_file='y'):
    #if not start_id:
    #    start_id=0
    #if count:
    #    end_id=int(start_id)+count
    #if end_id:
    #    filename=f"echr_metadata_{start_id}-{end_id}"
    #else:
    #    filename = f"echr_metadata_{start_id}-ALL"
    if start_date and end_date:
        filename = f"echr_metadata_{start_date}-{end_date}"
    elif start_date:
        filename = f"echr_metadata_{start_id}-END"
    elif end_date:
        filename = f"echr_metadata_START-{end_id}"
    else:
        filename = f"echr_metadata_START-END"
    print("--- STARTING ECHR DOWNLOAD ---")
    #df, resultcount = read_echr_metadata(end_id=end_id,start_id=start_id,verbose=False)
    df, resultcount = read_echr_metadata(start_id=start_id, end_id=end_id, start_date=start_date, end_date=end_date, verbose=verbose, skip_missing_dates=skip_missing_dates)
    if df is False and resultcount is False:
        return False
    if save_file == "y":
        # saving file
        Path('data').mkdir(parents=True, exist_ok=True)
        file_path = os.path.join('data', filename + '.csv')
        df.to_csv( file_path,index=False)
        print("\n--- DONE ---")
        return df
    else:
        print("\n--- DONE ---")
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
    print("Full-text download will now begin")
    if df is False:
        return False,False
    json_list = download_full_text_main(df,threads)
    print("Full-text download finished")
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

