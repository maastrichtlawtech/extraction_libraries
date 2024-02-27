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
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        div=parser.find_all('table')
        one=[]
        for divs in div:
            table=divs.find('table')
            if  table!=None:
                p=table.find_all('p',class_="coj-normal")
                for x in p:
                    span=x.find_all('span',class_="coj-bold")
                    for y in span:
                        if x!=None and y!=None:
                    # print(span.text)
                            one.append(y.text)
        return one            
                

    def html_page_structure_two(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
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
                        # print(op.text)
                        two.append(op.text)
        return two          
        
    def structure_three(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        table=parser.find_all('table')
        three=[]
        for tables in table:
            interior=tables.find_all('table')
            for interiors in interior:
                if interiors!=None:
                    p=interiors.find_all('p',class_="coj-normal")
                    for x in p:
                        span=x.find_all('span',class_="coj-bold")
                        for y in span:
                            if x!=None and y!=None:
                    # print(span.text)
                                three.append(y.text)
        return three            


        
    def structure_four(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
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
                                # print(subsequent.text)
                                four.append(subsequent.text)

                        
        return four     
        
    def structure_five(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
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
                                # print(subsequent.text)
                                five.append(subsequent.text)

                        
        return five 
    def structure_six(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        div=parser.find_all('h2')
        six=[]
        for h2 in div:
            # print(h2.text)
            if h2.text=="Operative part":
                operatives=h2.find_all_next('p')
                for operative in operatives:
                    # print(operative.text)
                    six.append(operative.text)
        return six     
    def structure_seven(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        div=parser.find_all('table')
        seven=[]
        for divs in div:
            table=divs.find_all('tbody')
            for tables in table:
                if  tables!=None:
                    p=tables.find_all('tr')
                    for x in p:
                        if x!=None:
                                td=x.find_all('td')
                                for y in td:
                                    if y!=None:
                                        p=y.find_all('p',class_="normal")
                                        for all in p:
                                            if all!=None:
                                                    span=all.find_all('span',class_="bold")
                                                    for spans in span:
                                                        #  print(spans.text)
                                                        seven.append(spans.text)
        return seven   
    def structure_eight(self)->list:  
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        tbody=parser.find_all('tbody')
        eight=[]
        for all in tbody:
            if all!=None:
                tr=all.find_all('tr')
                for trs in tr:
                    if trs!=None:
                        # print(trs)

                        p=parser.find_all('p',class_="normal")
                        for paras in p:
                            if paras!=None:
                                if "on those grounds" in paras.text.lower():

                                    span=paras.find_all_next('span',class_="bold")
                                    for spans in span:
                                        if spans!=None:
                                            eight.append(spans.text)
                                            # print(spans.text)

        return eight   
    def structure_nine(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        nine=[]
        div=parser.find_all('p')
        for divs in div:
                if divs!=None:
                        if "on those grounds" in divs.text.lower():
                                b=divs.find_all_next('b')
                                for bolds in b:
                                        # print(bolds.text)
                                        nine.append(bolds.text)
        return nine 
    def structure_eleven(self)->list:
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        bold = parser.find_all('b')

        eleven=[]
        
        # print(website)

        for b in bold:
            if b!=None:
                if "operative part" in b.text.lower():
                    table=b.find_all_next('p')
                    for tables in table:
                        if tables!=None:
                            eleven.append(tables.text)
                            # print(tables.text)
                    
                   
        
        return eleven
    def structure_ten(self):
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        appender=[]
        for string in parser.stripped_strings:
            # print(string)
            appender.append(string)
        # print(appender)

        found = False
        afterGrounds = []

        for x in appender: 

            if "on those grounds" in x.lower():
                found = True
                # print("True")

            if found:
                if len(x.split(" "))>3:
                    afterGrounds.append(x)
        return afterGrounds 
    def __call__(self)->list:
        one:list
        one=self.html_page_structure_one()
        if len(one)==0 or len(one)=="\n":
            one=self.html_page_structure_two()
            if len(one)==0 or one[0]=="\n":
                one=self.structure_three()
                if len(one)==0 or one[0]=="\n":
                    one=self.structure_four()
                    if len(one)==0 or one[0]=="\n":
                        one=self.structure_five()
                        if len(one)==0 or one[0]=="\n":
                            one=self.structure_six()
                            if len(one)==0 or one[0]=="\n":
                                one=self.structure_seven()
                                if len(one)==0 or one[0]=="\n":
                                    one=self.structure_eight()
                                    if len(one)==0 or one[0]=="\n":
                                        one=self.structure_nine()
                                        if len(one)==0 or one[0]=="\n":
                                            one=self.structure_ten()
                                            if len(one)==0 or one[0]=="\n":
                                                one=self.structure_eleven()
        return one               
                        


        
        
        
instance=Analyzer("61980CJ0027")
x=instance()   
if x!=None:
    print(x)



