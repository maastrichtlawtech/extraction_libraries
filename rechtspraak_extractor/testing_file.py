from rechtspraak_extractor.rechtspraak import get_rechtspraak
from rechtspraak_extractor.rechtspraak_metadata import get_rechtspraak_metadata
df = get_rechtspraak(sd='2025-01-01',
                     ed='2025-01-10',
                     save_file='n',
                     max_ecli=1000)
df_2 = get_rechtspraak_metadata(save_file='n',
                                dataframe=df,
                                _fake_headers=True)
print(len(df_2), len(df))
df_2.to_csv('data/test.csv', index=False, encoding='utf8')
# b = 2
pass
