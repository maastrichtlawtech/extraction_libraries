import requests
from bs4 import BeautifulSoup

def get_citations_from_celex_id(celex)->list:#Get  citations(Celex ID) from a website by providing celex ID in the function upon calling and reutrns a list of citations if exists else it returns an empty list
    website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:{celex}").text
    parser=BeautifulSoup(website,'lxml')
    div=parser.find_all('div',class_="panel-body")
    citations=[]
    for divs in div:
        if divs!=None:
            dl=divs.find('dl',class_="NMetadata")
            if dl!=None:
                dt=dl.find_all('dt')
                for dls in dl:
                    if "cited" in dls.text.lower():


                        temp=dls.find_all_next('dd')
                        for dd in temp:
                            if dd!=None:
                                li=dd.find_all('li')
                                for mentions in li:
                                    if mentions!=None:
                                        a=mentions.find('a')
                                        if a!=None:
                                            
                                          citations.append(a.text)
                                        # print(a.text)
    # print(citations)  
    filtered=[]      
    for splits in citations:
        if len(splits.split(" "))<2:
            filtered.append(splits)
             
    return filtered                                 

                                
sample=get_citations_from_celex_id("61962CJ0026")
print(sample)