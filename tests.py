from cellar_extractor import *
from echr_extractor import *
from rechtspraak_extractor import *

def echr_y():
    get_echr(save_file='y',count=100,start_date='2022-01-01')

def echr_n():
    get_echr(save_file='n',count=100,start_date='2022-01-01')

def echr_extra_y():
    get_echr_extra(save_file='n',count=100,start_date='2022-01-01')

def echr_extra_n():
    get_echr_extra(save_file='n',count=100,start_date='2022-01-01')

def rechtspraak_n():
    df = get_rechtspraak(max_ecli=100,sd='2022-01-01',save_file='n')
    get_rechtspraak_metadata(save_file='n',dataframe=df)

def rechtspraak_y():
    df = get_rechtspraak(max_ecli=100,sd='2022-01-01',save_file='y')
    get_rechtspraak_metadata(save_file='y',dataframe=df)

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


def test_echr_extra_y():
    try:
        echr_extra_y()
        assert True
    except Exception:
        assert False, "Saving extra cellar failed"

def test_echr_extra_n():
    try:
        echr_extra_n()
        assert True
    except Exception:
        assert False, "Saving extra cellar failed"

def test_echr_y():
    try:
        echr_y()
        assert True
    except Exception:
        assert False, "Saving extra cellar failed"

def test_echr_n():
    try:
        echr_n()
        assert True
    except Exception:
        assert False, "Saving extra cellar failed"

def test_rechtspraak_y():
    try:
        rechtspraak_y()
        assert True
    except Exception:
        assert False, "Saving extra cellar failed"

def test_rechtspraak_n():
    try:
        rechtspraak_n()
        assert True
    except Exception:
        assert False, "Saving extra cellar failed"
