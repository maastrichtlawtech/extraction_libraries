from echr_extractor.echr import get_echr
from echr_extractor.ECHR_html_downloader import download_full_text_main



if __name__ == '__main__':
    df = get_echr(count=100,save_file='n')
    full_text = download_full_text_main(df,10)
    b=2