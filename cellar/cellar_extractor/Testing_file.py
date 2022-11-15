"""

This file is purely a testing file for trying out separate parts of code, testing if everything works and such.
Can be also used to develop future code.

Current main usage - Setting up Storage -> Setting up all the folders in root directory.



"""


from helpers.json_to_csv import read_csv
from helpers.sparql import *
from helpers.citations_adder import add_citations_separate_webservice
if __name__ == '__main__':

   """
   CELEXES FOR TESTING USE
   62005TJ0321
   62006CO0415
    62000CJ0129
   They all have keywords and a summary
   """
   "62012CC0047"
   path="helpers\data\cellar_csv_data_clean.csv"
   data=read_csv(path)
   #celex="62021CO0659"
   username="n00ac9w5"
   password=""
   #celexes=["62021CO0659","62020CO0099","62021CO0221"]
   #query= " SELECT CI, DN WHERE DN = 62006CO0415"
   #response = run_eurlex_webservice_query(query,username,password
   add_citations_separate_webservice(data, 15, username, password)
   b=2