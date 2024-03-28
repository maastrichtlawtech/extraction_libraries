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
import unittest
from operative_extraction import Analyzer
# from test import testing
import random
import csv
file=open("gijs_202310_node_list.tsv","r")
reader=csv.reader(file)
no_of_test_cases=30
testing=[]
for row in reader:
    for rows in row:
        if "Id" not in rows:
            testing.append(rows.split("\t")[0])
            
class Test(unittest.TestCase):
    """
    class for unittesing operative part , it checks whether the list returns null value 
    or has some value.
    """
    ids:list
    
    def __init__(self,ids):
        self.ids=ids

    def test_for_celex_id(self):
        """
        Main function which runs the unittest Testcase .
        """
        count_fail:int
        count_pass=0
        for id in self.ids:
            test_output=Analyzer(id)
            test_instance=test_output()
         
            # self.assertFalse(len(test_instance)<=1)
          
            try:
                self.assertTrue(test_instance[0],f"{id} is not empty and has operative part")
                count_pass+=1 
                print(f"{id} --->  PASSED.")
            except:
                print(f"{id} --->  FAILED.")
        print(f"Passed {count_pass}/{len(self.ids)} times")
        # print(len(self.ids)-count,"were passed successfully")

new_list=[]
for w in range(no_of_test_cases):
    randomized=random.randint(0,len(testing)-1)
    new_list.append(testing[randomized])

if __name__ == '__main__':
   celex = "62004CJ0292"
    
   instance=Test([celex])
   instance.test_for_celex_id()  
   site = get_entire_page(celex)
   text = get_full_text_from_html(site)
   cits = get_citations_with_extra_info(text)
   print(cits)
   data,d2 = get_cellar_extra(sd='2023-01-01',max_ecli=100,save_file='n')
   nodes_edges = get_nodes_and_edges_lists(data)
   pass