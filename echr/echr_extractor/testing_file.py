import sys
from os.path import abspath

import echr_extractor

current_dir = (abspath(__file__))
correct_dir = '\\'.join(current_dir.replace('\\', '/').split('/')[:-2])
sys.path.append(correct_dir)
# print(sys.path)


if __name__ == '__main__':
    link = 'https://hudoc.echr.coe.int/#{"fulltext":["(NOT%20\"has%20been%20a%20violation%20of%20Article%206\")%20AND%20(\"has%20been%20no%20violation%20of%20Article%206\")"],"documentcollectionid2":["GRANDCHAMBER","CHAMBER"],"scl":["hatton"]}'
    df = echr_extractor.get_echr(link=link)
    b = 2
