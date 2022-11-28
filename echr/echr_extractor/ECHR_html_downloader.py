from bs4 import BeautifulSoup
import requests

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
import threading

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
    length = item_ids.size
     # to avoid getting problems with small files
    at_once_threads = int(length / threads)

    all_dict = list()
    threads = []
    for i in range(0, length, at_once_threads):
        curr_ids = item_ids[i:(i + at_once_threads)]
        t = threading.Thread(target=download_full_text_separate, args=(curr_ids, all_dict))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    main_dict = dict()
    for d in all_dict:
        main_dict.update(d)
    return main_dict


def download_full_text_separate(item_ids, dict_list):
    def download_html(item_ids):
        retry_ids = []
        htmls = {}
        for counter, item_id in enumerate(item_ids):
            #if counter % 100 == 0:
             #   print(f'{counter}/{len(item_ids)} items processed ...')
            try:
                r = requests.get(base_url + item_id, timeout=1)
                #print(base_url + item_id)
                htmls[item_id] = get_full_text_from_html(r.text)
            except Exception as e:
                retry_ids.append(item_id)

        return htmls, retry_ids

    dictionary, retry_ids = download_html(item_ids)
    dictionary_retry, r_id = download_html(retry_ids)
    dictionary.update(dictionary_retry)

    dict_list.append(dictionary)
