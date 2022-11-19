from cellar_extractor.json_to_csv import read_csv
from cellar_extractor.fulltext_saving import add_sections
from cellar_extractor.citations_adder import add_citations_separate_webservice


def extra_cellar(data=None, filepath=None, threads=10, username="", password=""):
    if data is None:
        data = read_csv(filepath)
    if filepath:
        if username !="" and password !="":
            add_citations_separate_webservice(data, username, password)
            print("Citations successfully added. The rest of additional extraction will now happen.")
        add_sections(data, threads, filepath.replace(".csv", "_fulltext.json"))
        data.to_csv(filepath, index=False)
    else:
        if username != "" and password != "":
            add_citations_separate_webservice(data, username, password)
            print("Citations successfully added. The rest of additional extraction will now happen.")
        json = add_sections(data, threads)
        return data, json
