from echr_extractor import *

def echr_y():
    get_echr(save_file='y',count=100,start_date='2022-01-01')

def echr_n():
    get_echr(save_file='n',count=100,start_date='2022-01-01')

def echr_extra_y():
    get_echr_extra(save_file='n',count=100,start_date='2022-01-01')

def echr_extra_n():
    get_echr_extra(save_file='n',count=100,start_date='2022-01-01')

def test_echr_extra_y():
    try:
        echr_extra_y()
        assert True
    except Exception:
        assert False, "Saving extra echr failed"

def test_echr_extra_n():
    try:
        echr_extra_n()
        assert True
    except Exception:
        assert False, "Downloading extra echr failed"

def test_echr_y():
    try:
        echr_y()
        assert True
    except Exception:
        assert False, "Saving echr failed"

def test_echr_n():
    try:
        echr_n()
        assert True
    except Exception:
        assert False, "Downloading echr failed"
