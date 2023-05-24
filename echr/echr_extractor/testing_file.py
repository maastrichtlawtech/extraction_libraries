import os,sys
from os.path import dirname, abspath
from pathlib import Path,PurePath

current_dir = (abspath(__file__))
correct_dir = '\\'.join(current_dir.replace('\\', '/').split('/')[:-2])
sys.path.append(correct_dir)
# print(sys.path)


from echr_extractor.echr import get_echr_extra, get_echr, get_nodes_edges
import dateutil.parser

import datetime
if __name__ == '__main__':
    df = get_echr_extra(count=100,save_file='y',language=["FRE","ENG"],start_date='2023-01-01')




    """
    Start and end dates must be date objects, which can be achieved by calling dateutil.parser.parse(some date string).date().
    I assume you dont want to do that in this file but im not sure where this conversion is most appropriate so I'll leave it up to you.
    Note that there is an extra import because of this.
    I have commented out some of your stuff to test this, if you run it as is it should work. @Benjamin
    """
    print(str(datetime.datetime.today().date()))
    #df = get_echr_extra(count=100,threads=5,start_date='2000-01-01',end_date='2023-01-01')
    #df,json = get_echr_extra(start_id=20,end_id=3000,save_file='n')

    #df = get_echr(start_id=1000,count=2000,save_file='n')

