from rechtspraak import *
from rechtspraak_metadata import *
df = get_rechtspraak(max_ecli=1000,save_file='n',sd='2021-01-01')
df_2 =get_rechtspraak_metadata(dataframe=df,save_file='n')
b=2