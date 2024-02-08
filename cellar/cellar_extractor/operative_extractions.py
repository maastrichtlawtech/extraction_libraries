import requests
from bs4 import BeautifulSoup
import unittest
# class ECLI():
#     ecli:str
#     def __init__(self,ecli):
#         self.ecli=ecli
class Analyzer():
    celex:str
    def __init__(self,celex):
        self.celex=celex
      

    def html_page_structure_one(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        div=parser.find_all('table')
        one=[]
        for divs in div:
            table=divs.find('table')
            if  table!=None:
                p=table.find('p',class_="coj-normal")
                span=p.find('span',class_="coj-bold")
                if p!=None and span!=None:
                    print(span.text)
                    one.append(span.text)
        return one            
                

    def html_page_structure_two(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        p=parser.find_all('p')
        two=[]
        for para in p:
            # print(para)
            span=para.find('span')
            if span!=None:
                # print(span.text)
                if "operative" in span.text.lower():
                    normal=span.find_all_next('p',class_="normal")
                    for op in normal:
                        print(op.text)
                        two.append(op.text)
        return two          
        
    def structure_three(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        table=parser.find_all('table')
        three=[]
        for tables in table:
            interior=tables.find_all('table')
            for interiors in interior:
                if interiors!=None:
                    p=interiors.find('p',class_="coj-normal")
                    span=p.find('span',class_="coj-bold")
                    if span!=None:

                        print(span.text)
                        three.append(span.text)
        return three            


        
    def structure_four(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        p=parser.find_all('p')
        four=[]
        for para in p:
            # print(para)
            span=para.find('span')
            if span!=None:
                # print(span.text)
                if "operative" in span.text.lower():
                    normal=span.find_all_next('table')
                    for op in normal:
                        tbody=op.find('tbody')
                        new_p=tbody.find_all('p',class_="oj-normal")
                        

                        for subsequent in new_p:
                            if subsequent!=None:
                                print(subsequent.text)
                                four.append(subsequent.text)

                        
        return four     
        
    def structure_five(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        p=parser.find_all('p')
        five=[]
        for para in p:
            # print(para)
            span=para.find('span')
            if span!=None:
                # print(span.text)
                if "operative" in span.text.lower():
                    normal=span.find_all_next('table')
                    for op in normal:
                        tbody=op.find('tbody')
                        new_p=tbody.find_all('p',class_="normal")
                        

                        for subsequent in new_p:
                            if subsequent!=None:
                                print(subsequent.text)
                                five.append(subsequent.text)

                        
        return five 
        
    def __call__(self)->list:
        one=self.html_page_structure_one()
        if len(one)==0:
            one=self.html_page_structure_two()
            if len(one)==0:
                one=self.structure_three()
                if len(one)==0:
                    one=one.structure_four()
                    if len(one)==0:
                        one=self.structure_five()
        print(one)                
                        


        pass
        
        
instance=Analyzer("3A62018CA0390")
instance()   



