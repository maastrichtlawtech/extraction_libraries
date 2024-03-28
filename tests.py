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
