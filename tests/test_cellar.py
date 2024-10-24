import random
from cellar_extractor import *


def cellar_csv_n():
    get_cellar(save_file="n", file_format="csv", sd="2022-01-01",
               max_ecli=100)


def cellar_csv_y():
    get_cellar(save_file="y", file_format="csv", sd="2022-01-01",
               max_ecli=100)


def cellar_json_n():
    get_cellar(save_file="n", file_format="json", sd="2022-01-01",
               max_ecli=100)


def cellar_json_y():
    get_cellar(save_file="y", file_format="json", sd="2022-01-01",
               max_ecli=100)


def cellar_extra_y():
    get_cellar_extra(save_file="y", max_ecli=10, sd="2022-01-01", threads=10)


def cellar_extra_n():
    get_cellar_extra(save_file="n", max_ecli=10, sd="2022-01-01", threads=10)


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


def operative_part_csv(celex):
    csv_store = Writing(celex)
    try:
        csv_store.to_csv()
        assert True
    except Exception:
        assert False, "Downloading and storing as csv failed\
              for operative part"


def operative_part_json(celex):
    json_store = Writing(celex)
    try:
        json_store.to_json()
        assert True
    except Exception:
        assert False, "Downloading and storing as json failed\
            for operative part"


def operative_part_txt(celex):
    txt_store = Writing(celex)
    try:
        txt_store.to_txt()
        assert True
    except Exception:
        assert False, "Downloading and storing as txt failed\
            for operative part"


def for_operative_part(celex):
    try:
        test_output = FetchOperativePart(celex)
        test_output()
        assert True
    except Exception:
        assert False, "Cannot extract for celex"


def test_operative_part_txt():
    celex_store = [
        "61983CJ0207",
        "61988CJ0360",
        "62005CJ0168",
        "62008CJ0484",
        "62010CJ0014",
        "62005CJ0343",
        "62000CJ0154",
    ]
    celex: str
    choice = random.randint(0, len(celex_store) - 1)
    celex = celex_store[choice]
    try:
        operative_part_txt(celex)
        assert True
    except Exception:
        assert False, "Cannot extract operative text"


def test_operative_part_json():
    celex_store = [
        "61983CJ0207",
        "61988CJ0360",
        "62005CJ0168",
        "62008CJ0484",
        "62010CJ0014",
        "62005CJ0343",
        "62000CJ0154",
    ]
    celex: str
    choice = random.randint(0, len(celex_store) - 1)
    celex = celex_store[choice]
    try:
        operative_part_json(celex)
        assert True
    except Exception:
        assert False, "Cannot extract operative text"


def test_operative_part_csv():
    celex_store = [
        "61983CJ0207",
        "61988CJ0360",
        "62005CJ0168",
        "62008CJ0484",
        "62010CJ0014",
        "62005CJ0343",
        "62000CJ0154",
    ]
    celex: str
    choice = random.randint(0, len(celex_store) - 1)
    celex = celex_store[choice]
    try:
        operative_part_csv(celex)
        assert True
    except Exception:
        assert False, "Cannot extract operative text"


def test_for_operative_part():
    celex_store = [
        "61983CJ0207",
        "61988CJ0360",
        "62005CJ0168",
        "62008CJ0484",
        "62010CJ0014",
        "62005CJ0343",
        "62000CJ0154",
    ]
    celex: str
    choice = random.randint(0, len(celex_store) - 1)
    celex = celex_store[choice]
    try:
        for_operative_part(celex)
        assert True
    except Exception:
        assert False, "Cannot extract operative part"
