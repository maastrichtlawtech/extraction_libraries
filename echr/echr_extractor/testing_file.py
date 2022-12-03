from echr_extractor.echr import get_echr,download_full_text
# from echr_extractor.echr_html_downloader import download_full_text_main



if __name__ == '__main__':
    df = get_echr(sd='2022-08-01', ed=None, count=100,save_file='n')
    full_text = download_full_text(df,10)