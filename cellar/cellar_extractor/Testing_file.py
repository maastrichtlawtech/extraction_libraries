"""

This file is purely a testing file for trying out separate parts of code, testing if everything works and such.
Can be also used to develop future code.



"""
from nodes_and_edges import get_nodes_and_edges
from os.path import join
from json_to_csv import read_csv
import time
from eurlex_scraping import  *
from cellar import *


def get_advocate_judge(text,phrase):
    try:
        index_matter = text.index(phrase)
        extracting = text[index_matter + len(phrase):]
        extracting = extracting.replace('\n','',1)
        ending = extracting.find('\n')
        extracting = extracting[:ending]
        extracting.replace(',','_') # In case they ever change it to delimeter
        subject_mat = extracting.split(sep="_")
        subject_mat = [i.strip() for i in subject_mat]
        subject = ";".join(subject_mat)
    except Exception:
        subject = ""
    return subject
def get_case_affecting(text):
    phrase = 'Case affecting:'
    try:
        index_matter = text.index(phrase)
        extracting = text[index_matter + len(phrase):]
        extracting = extracting.replace('\n','',1)
        phrases = extracting.split(sep='\n')
        good_one=[]
        for p in phrases:
            if ':' in p:
                break
            else:
                good_one.append(p)
        ids=[]
        for p in good_one:
            words = p.split()
            for w in words:
                if is_celex_id(w):
                    ids.append(w)
                    break

        return ';'.join(ids)
    except Exception:
        subject = ""
    return subject
if __name__ == '__main__':
  #  data = get_cellar(sd='1500-01-01',save_file='n',max_ecli=10000)
    entire_page = get_entire_page('62005CC0335')
    text = get_full_text_from_html(entire_page)
    adv = get_advocate_judge(text,"Advocate General:")
    judge = get_advocate_judge(text,"Judge-Rapporteur:")
    case_affecting = get_case_affecting(text)
    print(adv)
    print(judge)
    print(case_affecting)
    b=2
    #get_cellar_extra(save_file="y",username="n00ac9w5",password="",max_ecli=100000000000,threads=15,sd="1900-01-01")
