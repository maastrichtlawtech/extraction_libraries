import json
import os
import time
from datetime import datetime
from pathlib import Path
import logging
from tqdm import tqdm

from cellar_extractor.cellar_extra_extract import extra_cellar
from cellar_extractor.cellar_queries import get_all_eclis, get_raw_cellar_metadata
from cellar_extractor.json_to_csv import json_to_csv_main, json_to_csv_returning
from cellar_extractor.nodes_and_edges import get_nodes_and_edges


def get_cellar(
    ed=None, save_file="y", max_ecli=100, sd="2022-05-01", file_format="csv"
):
    if not ed:
        ed = datetime.now().isoformat(timespec="seconds")
    file_name = "cellar_" + sd + "_" + ed
    file_name = file_name.replace(":", "_")
    logging.info("\n--- PREPARATION ---\n")
    logging.info(f"Starting from specified start date: {sd}")
    logging.info(f"Up until the specified end date {ed}")
    eclis = get_all_eclis(starting_date=sd, ending_date=ed)
    logging.info(f"Found {len(eclis)} ECLIs")
    time.sleep(1)
    if len(eclis) > max_ecli:
        eclis = eclis[:max_ecli]
    if len(eclis) == 0:
        logging.info(f"No data to download found between {sd} and {ed}")
        return False
    all_eclis = {}
    concurrent_docs = 100
    for i in tqdm(range(0, len(eclis), concurrent_docs), colour="GREEN"):
        new_eclis = get_raw_cellar_metadata(eclis[i : (i + concurrent_docs)])
        all_eclis = {**all_eclis, **new_eclis}
    if save_file == "y":
        Path("data").mkdir(parents=True, exist_ok=True)
        if file_format == "csv":
            file_path = os.path.join("data", file_name + ".csv")
            json_to_csv_main(all_eclis, file_path)
        else:
            file_path = os.path.join("data", file_name + ".json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(all_eclis, f)
    else:
        if file_format == "csv":
            df = json_to_csv_returning(all_eclis)
            return df
        else:
            return all_eclis
    logging.info("\n--- DONE ---")


def get_cellar_extra(
    ed=None,
    save_file="y",
    max_ecli=100,
    sd="2022-05-01",
    threads=10,
    username="",
    password="",
):
    if not ed:
        ed = datetime.now().isoformat(timespec="seconds")
    data = get_cellar(ed=ed, save_file="n", max_ecli=max_ecli, sd=sd, file_format="csv")
    if data is False:
        logging.warning("Cellar extraction unsuccessful")
        return False, False
    logging.info("\n--- START OF EXTRA EXTRACTION ---")
    file_name = "cellar_extra_" + sd + "_" + ed
    file_name = file_name.replace(":", "_")
    file_path = os.path.join("data", file_name + ".csv")
    if save_file == "y":
        Path("data").mkdir(parents=True, exist_ok=True)
        extra_cellar(
            data=data,
            filepath=file_path,
            threads=threads,
            username=username,
            password=password,
        )
        logging.info("\n--- DONE ---")

    else:
        data, json_data = extra_cellar(
            data=data, threads=threads, username=username, password=password
        )
        logging.info("\n--- DONE ---")

        return data, json_data


def get_nodes_and_edges_lists(df=None, only_local=False):
    if df is None:
        logging.warning("No dataframe passed!")
        return
    try:
        nodes, edges = get_nodes_and_edges(df, only_local)
    except:
        logging.warning("Something went wrong. Nodes and edges creation unsuccessful.")
        return False, False
    return nodes, edges


def filter_subject_matter(df=None, phrase=None):
    if df is None or phrase is None:
        logging.info("Incorrect input values! \n Returning... \n")
    else:
        try:
            mask = (
                df["LEGAL RESOURCE IS ABOUT SUBJECT MATTER"]
                .str.lower()
                .str.contains(phrase.lower(), na=False)
            )
            return df[mask]
        except Exception as e:
            logging.warning(e)
            logging.warning("Something went wrong!\n Returning... \n")
            return None
