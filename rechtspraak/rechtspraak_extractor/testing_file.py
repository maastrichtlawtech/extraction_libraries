from rechtspraak import *
from rechtspraak_metadata import *
df = get_rechtspraak(ed='1995-01-01',save_file='y',max_ecli=100)
df_2 = get_rechtspraak_metadata(save_file='y')
b=2
pass