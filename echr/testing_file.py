from echr_extractor.echr import get_echr
from echr_extractor.ECHR_html_downloader import metadata_to_html



if __name__ == '__main__':
    df = get_echr(count=100,save_file='n')
    full_text = metadata_to_html(df)
    b=2