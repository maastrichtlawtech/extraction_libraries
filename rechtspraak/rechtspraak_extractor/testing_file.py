from rechtspraak import *
from rechtspraak_metadata import *
df = get_rechtspraak(max_ecli=100,sd='2022-01-01',save_file='y')
get_rechtspraak_metadata(save_file='y',dataframe=df)
pass