import requests
from bs4 import BeautifulSoup

def get_para_citations_from_celex_id(celex)->list:#Get paragraph citations from a website by providing celex ID in the function upon calling and reutrns a list of citations if exists else it returns an empty list
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
                                        if "p" in mentions.text.lower().split(" "):
                                        
                                       
                                            # print(mentions.text)    
                                            citations.append(mentions.text)
                                        # print(a.text)
    # print(citations)  
    filtered=[]      
    for splits in citations:
       
        filtered.append(splits.split(":")[1])
             
    return filtered                               
    
sample=get_para_citations_from_celex_id("61962CJ0026")
print(sample)