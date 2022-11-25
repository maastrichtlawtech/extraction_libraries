import sys
import pathlib
from echr import get_echr

df = get_echr(sd='2022-08-01', ed=None,count=10, save_file='y')

# print(df.head(5))