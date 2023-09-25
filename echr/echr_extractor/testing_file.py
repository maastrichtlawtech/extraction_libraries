import sys
from os.path import abspath

import echr_extractor

current_dir = (abspath(__file__))
correct_dir = '\\'.join(current_dir.replace('\\', '/').split('/')[:-2])
sys.path.append(correct_dir)
# print(sys.path)


if __name__ == '__main__':
    link = 'https://hudoc.echr.coe.int/#{"fulltext":["\"prison%20sentence\"%20AND%20here"],"documentcollectionid2":["GRANDCHAMBER","CHAMBER"]}'
    df = echr_extractor.get_echr(link = link)
    b=2