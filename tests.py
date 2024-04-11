from cellar_extractor import *

def cellar_csv_n():
    get_cellar(save_file='n', file_format='csv', sd='2022-01-01', max_ecli=100)


def cellar_csv_y():
    get_cellar(save_file='y', file_format='csv', sd='2022-01-01', max_ecli=100)


def cellar_json_n():
    get_cellar(save_file='n', file_format='json', sd='2022-01-01', max_ecli=100)


def cellar_json_y():
    get_cellar(save_file='y', file_format='json', sd='2022-01-01', max_ecli=100)


def cellar_extra_y():
    get_cellar_extra(save_file='y', max_ecli=10, sd='2022-01-01', threads=10)


def cellar_extra_n():
    get_cellar_extra(save_file='n', max_ecli=10, sd='2022-01-01', threads=10)


def test_cellar_extra_y():
    try:
        cellar_extra_y()
        assert True
    except Exception:
        assert False, "Saving extra cellar failed"


def test_cellar_extra_n():
    try:
        cellar_extra_n()
        assert True
    except Exception:
        assert False, "Downloading extra cellar failed"


def test_cellar_csv_y():
    try:
        cellar_csv_y()
        assert True
    except Exception:
        assert False, "Saving cellar as csv failed."


def test_cellar_csv_n():
    try:
        cellar_csv_n()
        assert True
    except Exception:
        assert False, "Downloading cellar as csv failed."


def test_cellar_json_y():
    try:
        cellar_csv_y()
        assert True
    except Exception:
        assert False, "Saving cellar as json failed."


def test_cellar_json_n():
    try:
        cellar_csv_y()
        assert True
    except Exception:
        assert False, "Downloading cellar as json failed."



import random
import csv
import json 

celex_store=["61983CJ0207","61988CJ0360","62005CJ0168","62008CJ0484","62010CJ0014","62005CJ0343","62000CJ0154"]

celex:str
choice=random.randint(0,len(celex_store))
celex=celex_store[choice]
def operative_part_csv(celex)->csv:

    csv_store=Writing(celex)
    csv_store.to_csv()
    if csv_store.to_csv():
        assert True
    else:
        assert False    
def operative_part_json(celex)->json:
    json_store=Writing(celex)
    json_store.to_json()
    if json_store.to_json():
        assert True
    else:
        assert False

def operative_part_txt(celex):
    txt_store=Writing(celex)
    txt_store.to_txt()
    if txt_store.to_txt():
        assert True
    else:
        assert False
