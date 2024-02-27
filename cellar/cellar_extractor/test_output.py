import csv
file=open("gijs_202310_node_list.tsv","r")
reader=csv.reader(file)
from output import Writing
testing=[]
for row in reader:
    for rows in row:
        if "Id" not in rows:
            testing.append(rows.split("\t")[0])
         
for all in testing:
    instance=Writing(all)
    instance()
    # print(all)