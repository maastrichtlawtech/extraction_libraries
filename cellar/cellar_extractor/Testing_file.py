"""

This file is purely a testing file for trying out separate parts of code, testing if everything works and such.
Can be also used to develop future code.

Current main usage - Setting up Storage -> Setting up all the folders in root directory.



"""


from helpers.citations_adder import *
from helpers.fulltext_saving import *
from helpers.eurlex_scraping import *
from helpers.json_to_csv import *
from helpers.sparql import *

if __name__ == '__main__':

   """
   CELEXES FOR TESTING USE
   62005TJ0321
   62006CO0415
    62000CJ0129
   They all have keywords and a summary
   """
   link="https://ereader.cambridge.org/wr/viewer.html#book/8130a37c-c063-43ad-847f-9ac5428123f1/doc1"
   celex="62021CO0659"
   username=""
   password=""
   celexes=["62021CO0659","62020CO0099","62021CO0221"]
   query= "SELECT DN WHERE DN = 62000CJ0129"
   response = get_keywords_from_celex(query,username,password)
   b=2
