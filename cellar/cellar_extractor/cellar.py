import json
import os
from datetime import date, datetime
from pathlib import Path

from cellar_queries import get_all_eclis, get_raw_cellar_metadata
from json_to_csv import json_to_csv_main, json_to_csv_returning


def get_cellar(ed=None, save_file='y', max_ecli=100, sd="2022-05-01", file_format='csv'):
    current_time = datetime.now().strftime("%H-%M-%S")
    if not ed:
        ed = date.today().strftime("%Y-%m-%d")

    file_name = 'cellar_' + sd + '_' + ed + '_' + current_time
    print('\n--- PREPARATION ---\n')
    print(f'Starting from specified start date: {sd}')
    print(f'Up until the specified end date {ed}')
    eclis = get_all_eclis(starting_date=sd, ending_date=ed)
    print(f"Found {len(eclis)} ECLIs")
    eclis = eclis[:max_ecli]

    all_eclis = {}
    concurrent_docs = 100
    for i in range(0, len(eclis), concurrent_docs):
        new_eclis = get_raw_cellar_metadata(eclis[i:(i + concurrent_docs)])
        all_eclis = {**all_eclis, **new_eclis}
    if save_file == 'y':
        Path('data').mkdir(parents=True, exist_ok=True)
        if file_format == 'csv':
            file_path = os.path.join('data', file_name + '.csv')
            json_to_csv_main(all_eclis, file_name, file_path)
        else:
            file_path = os.path.join('data', file_name + '.json')
            with open(file_path, "w") as f:
                json.dump(all_eclis, f)
    else:
        if file_format == 'csv':
            df = json_to_csv_returning(all_eclis)
            return df
        else:
            return all_eclis
    print("\n--- DONE ---")
