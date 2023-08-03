"""

This file is purely a testing file for trying out separate parts of code, testing if everything works and such.
Can be also used to develop future code.



"""

from nodes_and_edges import get_nodes_and_edges
from os.path import join
from json_to_csv import read_csv
import time
from eurlex_scraping import *
from cellar import *
from sparql import *




if __name__ == '__main__':
   celex = "62004CJ0292"
   site = get_entire_page(celex)
   text = get_full_text_from_html(site)
   cits = get_citations_with_extra_info(text)
   print(cits)
   data,d2 = get_cellar_extra(sd='2023-01-01',max_ecli=100,save_file='n')
   d3 = filter_subject_matter(data, "prices")
   b=2
   pass