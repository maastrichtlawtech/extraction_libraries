from json_to_csv import read_csv
from fulltext_saving import add_sections

def extra_cellar(data=None,filepath=None, threads=10):
    if not data:
        data = read_csv(filepath)
    if filepath:
        add_sections(data, threads, filepath.replace(".csv", "_fulltext.json"))
        data.to_csv(filepath, index=False)
    else:
        json = add_sections(data, threads)
        return data, json
