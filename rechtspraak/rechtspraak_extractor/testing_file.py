from rechtspraak import get_rechtspraak
from rechtspraak_metadata import get_rechtspraak_metadata
df = get_rechtspraak(ed='2025-01-01',
                     save_file='y',
                     max_ecli=10000)
df_2 = get_rechtspraak_metadata(save_file='y')
b = 2
pass
