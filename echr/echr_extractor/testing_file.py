import logging
import sys
from os.path import abspath

import echr_extractor

current_dir = (abspath(__file__))
correct_dir = '\\'.join(current_dir.replace('\\', '/').split('/')[:-2])
sys.path.append(correct_dir)
# print(sys.path)


if __name__ == '__main__':
    link = 'https://hudoc.echr.coe.int/eng#%7B%22fulltext%22:[%22(NOT%20%5C%22has%20been%20a%20violation%20of%20Article%206%5C%22)%20AND%20(%5C%22has%20been%20no%20violation%20of%20Article%206%5C%22)%22]%7D'
    logging.info('hey')
    df = echr_extractor.get_echr(link=link)
    b = 2
