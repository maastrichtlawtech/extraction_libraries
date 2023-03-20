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


if __name__ == '__main__':
    data,full= get_cellar_extra(sd='2023-01-01',save_file='n',max_ecli=300)
    b=2