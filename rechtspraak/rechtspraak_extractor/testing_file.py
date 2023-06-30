from rechtspraak import *
from rechtspraak_metadata import *
df = get_rechtspraak(ed='1995-01-01',save_file='n',max_ecli=1000000)
df_2 = get_rechtspraak_metadata(save_file='n',dataframe=df)
b=2
pass