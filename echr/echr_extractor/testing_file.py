import logging
import sys
from os.path import abspath

import echr_extractor

current_dir = (abspath(__file__))
correct_dir = '\\'.join(current_dir.replace('\\', '/').split('/')[:-2])
sys.path.append(correct_dir)
# print(sys.path)


if __name__ == '__main__':
    payload = 'contentsitename:ECHR AND (NOT (doctype=PR OR doctype=HFCOMOLD OR doctype=HECOMOLD)) AND ((NOT "has been a violation of Article 6") AND ("has been no violation of Article 6")) AND ((languageisocode="ENG")) AND ((documentcollectionid="GRANDCHAMBER") OR (documentcollectionid="CHAMBER"))'
    df = echr_extractor.get_echr(query_payload=payload)
    b = 2
