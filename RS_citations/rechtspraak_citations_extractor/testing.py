import pandas as pd


from citations_extractor import get_citations

if __name__ == '__main__':
    name = 'rechtspraak_2018-01-01_2023-06-02_17-45-29_metadata.csv'
    data = pd.read_csv(name)
    df = get_citations(data,'','',2)
    b=2