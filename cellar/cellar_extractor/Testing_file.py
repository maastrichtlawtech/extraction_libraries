"""

This file is purely a testing file for trying out separate parts of code, testing if everything works and such.
Can be also used to develop future code.



"""
from nodes_and_edges import get_nodes_and_edges
from os.path import join
from json_to_csv import read_csv
import time
from cellar import get_cellar
if __name__ == '__main__':
    data = get_cellar(sd='1500-01-01',save_file='n',max_ecli=100)
    path = join("","data")
    path_file = join(path,"cellar_full_january_2023.csv")
    df = read_csv(path_file)
    nodes,edges = get_nodes_and_edges(df)
    path_nodes = join(path, "nodes.csv")
    path_edges = join(path, "edges.csv")
    nodes.to_csv(path_nodes,index=False)
    edges.to_csv(path_edges,index=False)


    #get_cellar_extra(save_file="y",username="n00ac9w5",password="",max_ecli=100000000000,threads=15,sd="1900-01-01")
