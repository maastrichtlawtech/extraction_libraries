import threading

import requests
from bs4 import BeautifulSoup

base_url = 'https://hudoc.echr.coe.int/app/conversion/docx/html/body?library=ECHR&id='


def get_full_text_from_html(html_text):
    # This method turns the html code from the summary page into text
    # It has different cases depending on the first character of the CELEX ID
    # Should only be used for summaries extraction
    soup = BeautifulSoup(html_text, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.replace(",", "_")
    return text


def download_full_text_main(df, threads):
    item_ids = df['itemid']
    eclis = df['ecli']
    length = item_ids.size
    if length > threads:
        at_once_threads = int(length / threads)
    else:
        at_once_threads = length
    all_dict = list()
    threads = []
    for i in range(0, length, at_once_threads):
        curr_ids = item_ids[i:(i + at_once_threads)]
        curr_ecli = eclis[i:(i + at_once_threads)]
        t = threading.Thread(target=download_full_text_separate, args=(curr_ids, curr_ecli, all_dict))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    json_file = list()
    for l in all_dict:
        if len(l) > 0:
            json_file.extend(l)
    return json_file


def download_full_text_separate(item_ids, eclis, dict_list):
    full_list = []
    eclis = eclis.reset_index(drop=True)
    item_ids = item_ids.reset_index(drop=True)

    def download_html(item_ids, eclis):
        retry_ids = []
        retry_eclis = []
        for i in range(len(item_ids)):
            item_id = item_ids[i]
            ecli = eclis[i]
            try:
                r = requests.get(base_url + item_id, timeout=1)
                json_dict = {
                    'item_id': item_id,
                    'ecli': ecli,
                    'full_text': get_full_text_from_html(r.text)
                }
                full_list.append(json_dict)
            except Exception:
                retry_ids.append(item_id)
                retry_eclis.append(ecli)
        return retry_ids, retry_eclis

    retry_ids, retry_eclis = download_html(item_ids, eclis)
    download_html(retry_ids, retry_eclis)
    dict_list.append(full_list)
