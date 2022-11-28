from echr_extractor.ECHR_metadata_harvester import read_echr_metadata
import time
from pathlib import Path
import os
def get_echr(sd='2022-08-01', ed=None,count=None, save_file='y'):

    print('\n--- START ---')

    print("--- Extract ECHR data")
    # arg_end_id = args.count if args.count else None
    df, resultcount = read_echr_metadata(end_id= count,
                                         verbose=True)
    print(f'ECHR data shape: {df.shape}')
    print(f'Columns extracted: {list(df.columns)}')

    file_name="extract"
    print("\n--- DONE ---")
    if save_file == "y":
        # saving file
        Path('data').mkdir(parents=True, exist_ok=True)
        file_path = os.path.join('data', file_name + '.csv')
        df.to_csv( file_path,index=False)
        return df
    else:
        return df


