from cellar_extractor.helpers.json_to_csv import read_csv
from cellar_extractor.helpers.fulltext_saving import add_sections

def extra_cellar(data=None,filepath=None, threads=10):
    print(f" Starting Extra cellar with {data} as data, {filepath} as filepath")
    if data is None:
        data = read_csv(filepath)
    if filepath:
        add_sections(data, threads, filepath.replace(".csv", "_fulltext.json"))
        data.to_csv(filepath, index=False)
    else:
        json = add_sections(data, threads)
        return data, json
