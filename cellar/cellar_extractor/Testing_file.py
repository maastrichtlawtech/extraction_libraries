"""

This file is purely a testing file for trying out separate parts of code, testing if everything works and such.
Can be also used to develop future code.

Current main usage - Setting up Storage -> Setting up all the folders in root directory.



"""
from os.path import join
from json_to_csv import read_csv
from cellar import get_cellar_extra
import math
if __name__ == '__main__':

    path = join("","data")
    path_file = join(path,"tester.csv")
    df = read_csv(path_file)
    b=2
    get_cellar_extra(sd="1900-01-01",ed="2020-01-01",max_ecli=350,threads=15,save_file="y",username="n00ac9w5",password="")