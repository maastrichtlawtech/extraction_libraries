import cellar_extractor as cell

Below are examples for in-memory saving:

df = cell.get_cellar(save_file='n', file_format='csv', sd='2022-01-01', max_ecli=100)
df,json = cell.get_cellar_extra(save_file='n', max_ecli=100, sd='2022-01-01', threads=10)

import rechtspraak_extractor as rex

 To get the rechtspraak data in a dataframe:
df = rex.get_rechtspraak(max_ecli=100, sd='2022-08-01', save_file='n')  
df_metadata = rex.get_rechtspraak_metadata(save_file='n', dataframe=df)
