import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

from citations_extractor import get_citations

if __name__ == '__main__':
    name = '../../data/rechtspraak_1900-01-01_2024-01-01_11-50-58.csv'
    data = pd.read_csv(name)
    username = os.getenv('LIDO-USERNAME')
    password = os.getenv('LIDO-PASSWORD')
    print(username, password)
    df = get_citations(data,username=username,password=password,threads=2)
    df.to_csv('../../data/citations.csv',index=False)