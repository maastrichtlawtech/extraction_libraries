from rechtspraak_extractor.rechtspraak import get_rechtspraak
from rechtspraak_extractor.rechtspraak_metadata import get_rechtspraak_metadata


def rechtspraak_n():
    df = get_rechtspraak(max_ecli=100, sd='2022-01-01', save_file='n')
    get_rechtspraak_metadata(save_file='n', dataframe=df)


def rechtspraak_y():
    df = get_rechtspraak(max_ecli=100, sd='2022-01-01', save_file='y')
    get_rechtspraak_metadata(save_file='y', dataframe=df)


def test_rechtspraak_y():
    try:
        rechtspraak_y()
        assert True
    except Exception:
        assert False, "Saving extra rechtspraak failed"


def test_rechtspraak_n():
    try:
        rechtspraak_n()
        assert True
    except Exception:
        assert False, "Downloading extra rechtspraak failed"
