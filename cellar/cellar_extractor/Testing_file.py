"""

This file is purely a testing file for trying out separate parts of code, testing if everything works and such.
Can be also used to develop future code.

Current main usage - Setting up Storage -> Setting up all the folders in root directory.



"""
from cellar import get_cellar_extra
if __name__ == '__main__':

    """
    CELEXES FOR TESTING USE
    62005TJ0321
    62006CO0415
     62000CJ0129
    They all have keywords and a summary
    """
    "6 2012 CC 0047"
    #path = "helpers\data\cellar_csv_data_clean.csv"
    #data = read_csv(path)
    # celex="62021CO0659"
    #username = "n00ac9w5"
    #password = ""
    #celexes = ['62021CO0659', "62020CO0099", "62021CO0221"]
    #prog = re.compile(r'^[1234567890CE]\d{4}[A-Z]{1,2}\d{4}\d*')
    #for id in celexes:
     #   result = prog.match(id)
     #   if result:
     #       print("works")
    #query= " SELECT CI, DN WHERE DN = 62019CJ0668"
    #response = run_eurlex_webservice_query(query,username,password)
    #add_citations_separate_webservice(data, 15, username, password)
    #b=2
    get_cellar_extra(sd="1999-01-01",max_ecli=1000000,threads=10,save_file="n",username="n00ac9w5",password="XUtjyPDrl1c")