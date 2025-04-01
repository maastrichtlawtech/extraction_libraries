from rechtspraak_extractor import get_rechtspraak
from rechtspraak_extractor.rechtspraak_metadata import get_rechtspraak_metadata
df = get_rechtspraak(sd='2025-01-01',
                     ed='2025-01-10',
                     save_file='y',
                     max_ecli=1000)
df_2 = get_rechtspraak_metadata(save_file='y', dataframe=df)
b = 2
pass
