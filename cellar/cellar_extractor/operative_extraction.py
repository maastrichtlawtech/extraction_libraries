import requests
from bs4 import BeautifulSoup
import unittest
from operative_extraction import Analyzer
import csv
import json
class Analyzer():
    """
    This class returns a list of the operative part for a given celex id . Celex id is initialized through a constructor.
    """
    celex:str # declare celex as a string
    def __init__(self,celex):# Initialize Celex id as a constructor , passed when calling the class
        self.celex=celex
      

    def html_page_structure_one(self)->list:
        """
         This function retreives operative part from documents of the respected celex id's . This function scrapes/parse the operative part from a nested
         table structure . The relevant text lies inside the coj-bold class of the span tag.
        """
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        div=parser.find_all('table') # Find all tables tag from the website
        one=[]
        for divs in div:
            table=divs.find('table') # Find each nested table within the table
            if  table!=None:
                p=table.find_all('p',class_="coj-normal") # Find all p under the nested table with the coj-normal class
                for x in p:
                    span=x.find_all('span',class_="coj-bold")# Span class of coj-bold under the p tag
                    for y in span:
                        if x!=None and y!=None:
                 
                            one.append(y.text)#append text from span onto a list
        return one            
                

    def html_page_structure_two(self)->list:
        """
         This function retreives operative part from documents of the respected celex id's . This function scrapes/parse the operative part from a paragraph
         (p) structure . The relevant text lies inside the normal class of the p tag which comes after the keyword operative of the previous span tag.
        """
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        p=parser.find_all('p')
        two=[]
        for para in p:
        
            span=para.find('span')
            if span!=None:
            
                if "operative" in span.text.lower():
                    normal=span.find_all_next('p',class_="normal")
                    for op in normal:
                    
                        two.append(op.text)
        return two          
        
    def structure_three(self)->list:
        """
         This function retreives operative part from documents of the respected celex id's . This function scrapes/parse the operative part from a nested
         table structure . The relevant text lies inside the coj-bold class of the span tag.
        """
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
                
                                three.append(y.text)
        return three            


        
    def structure_four(self)->list:
        """
         This function retreives operative part from documents of the respected celex id's . This function scrapes/parse the operative part from a paragraph
         (p) structure . The relevant text lies inside the p  tag which comes after the keyword operative of the previous span tag.
        """
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        p=parser.find_all('p')
        four=[]
        for para in p:
         
            span=para.find('span')
            if span!=None:
         
                if "operative" in span.text.lower():
                    normal=span.find_all_next('table')
                    for op in normal:
                        tbody=op.find('tbody')
                        new_p=tbody.find_all('p',class_="oj-normal")
                        

                        for subsequent in new_p:
                            if subsequent!=None:
                        
                                four.append(subsequent.text)

                        
        return four     
        
    def structure_five(self)->list:
        
        """
         This function retreives operative part from documents of the respected celex id's . This function scrapes/parse the operative part from a paragraph
         (p) structure . The relevant text lies inside the normal class of the p tag which comes after the keyword operative of the previous span tag.
        """
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        p=parser.find_all('p')
        five=[]
        for para in p:
      
            span=para.find('span')
            if span!=None:
         
                if "operative" in span.text.lower():
                    normal=span.find_all_next('table')
                    for op in normal:
                        tbody=op.find('tbody')
                        new_p=tbody.find_all('p',class_="normal")
                        

                        for subsequent in new_p:
                            if subsequent!=None:
                               
                                five.append(subsequent.text)

                        
        return five 
    def structure_six(self)->list:
        """
         This function retreives operative part from documents of the respected celex id's . This function scrapes/parse the operative part from a h2
         (header) structure . The relevant text lies inside thee p tag which comes after the keyword operative part of the respective h2  tag.
         """
        
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        div=parser.find_all('h2')
        six=[]
        for h2 in div:
            # print(h2.text)
            if h2.text=="Operative part":
                operatives=h2.find_all_next('p')
                for operative in operatives:
                    
                    six.append(operative.text)
        return six     
    def structure_seven(self)->list:
        """
         This function retreives operative part from documents of the respected celex id's . This function scrapes/parse the operative part from a table
         (table) structure . The relevant text lies inside the span tag which comes after the p tag , with the class name=normal.
        """
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        div=parser.find_all('table')
        seven=[]
        for divs in div:
            # find tbody within the table
            table=divs.find_all('tbody')
            for tables in table:
                if  tables!=None:
                    # find tr within the tbody
                    p=tables.find_all('tr')
                    for x in p:
                        if x!=None:
                                # find td within the tr
                                td=x.find_all('td')
                                for y in td:
                                    if y!=None:
                                        p=y.find_all('p',class_="normal")
                                        for all in p:
                                            if all!=None:
                                                    # find operative part within the span
                                                    span=all.find_all('span',class_="bold")
                                                    for spans in span:
                                                        # APpend it into a list and return the list when the function is called
                                                        seven.append(spans.text)
        return seven   
    def structure_eight(self)->list:  
        """
         This function retreives operative part from documents of the respected celex id's .The text is extracted from the span tag nested inside 
         the tbody tag.Returns a list as output.
        """
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        
        tbody=parser.find_all('tbody')
        eight=[]
        for all in tbody:
            if all!=None:
                tr=all.find_all('tr')
                for trs in tr:
                    if trs!=None:
                       

                        p=parser.find_all('p',class_="normal")
                        for paras in p:
                            if paras!=None:
                                if "on those grounds" in paras.text.lower():

                                    span=paras.find_all_next('span',class_="bold")
                                    for spans in span:
                                        if spans!=None:
                                            eight.append(spans.text)
                                           

        return eight   
    def structure_nine(self)->list:
        """
         This function retreives operative part from documents of the respected celex id's .The operative part is under the bold(b)
         tag after the p tag where the keywords "on those grounds" exist. 
        """
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
        """
         This function retreives operative part from documents of the respected celex id's .The operative part is under the paragraph(p)
         tag after the b tag where the keywords "operative part" exist. 
        """
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        bold = parser.find_all('b')

        eleven=[]
        
    

        for b in bold:
            if b!=None:
                if "operative part" in b.text.lower():
                    table=b.find_all_next('p')
                    for tables in table:
                        if tables!=None:
                            eleven.append(tables.text)
                       
                    
                   
        
        return eleven
    def structure_ten(self):
        """
         This function retreives operative part from documents of the respected celex id's Since the ocntent is preloaded using js/client s
         server side functions , the text from the current page is retrieved and the operative part is scraped after the occurence of the phrase
         "On those grounds".
        """
        website=requests.get(f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A{self.celex}&from=EN").text
        parser=BeautifulSoup(website,'lxml')
        appender=[]
        for string in parser.stripped_strings:
       
            appender.append(string)


        found = False
        afterGrounds = []

        for x in appender: 

            if "on those grounds" in x.lower():
                found = True
            

            if found:
                if len(x.split(" "))>3:
                    afterGrounds.append(x)
        return afterGrounds 
    def __call__(self)->list:
        """
        This inbuilt __call__ function loops through all the methods in the class `Analyzer` and returns  the list , with values of the operative part .
        """
       
        container=[self.html_page_structure_one(),self.html_page_structure_two(),self.structure_three(),self.structure_four(),self.structure_five(),
                   self.structure_six(),self.structure_seven(),self.structure_eight(),self.structure_nine(),self.structure_ten(),self.structure_eleven()]
        
       
      
        one:list
        for funcs in range(len(container)):
          
            one=container[funcs]
          
            if one:
                if (len(one)!=0 or one[0]!="\n"):
                    print("here")
                    return one


          

                
            
        # one=self.html_page_structure_one()
        # if len(one)==0 or len(one)=="\n":
        #     one=self.html_page_structure_two()
        #     if len(one)==0 or one[0]=="\n":
        #         one=self.structure_three()
        #         if len(one)==0 or one[0]=="\n":
        #             one=self.structure_four()
        #             if len(one)==0 or one[0]=="\n":
        #                 one=self.structure_five()
        #                 if len(one)==0 or one[0]=="\n":
        #                     one=self.structure_six()
        #                     if len(one)==0 or one[0]=="\n":
        #                         one=self.structure_seven()
        #                         if len(one)==0 or one[0]=="\n":
        #                             one=self.structure_eight()
        #                             if len(one)==0 or one[0]=="\n":
        #                                 one=self.structure_nine()
        #                                 if len(one)==0 or one[0]=="\n":
        #                                     one=self.structure_ten()
        #                                     if len(one)==0 or one[0]=="\n":
        #                                         one=self.structure_eleven()
                     
                        


        
        
        
# instance=Analyzer("61962CJ0026")
# x=instance()   
# if x!=None:
#     print(x)


class Writing():
    """
    This class has different methods , for the purpose of writing the operative part into different file formats.(Csv,txt,json)
    """
    
    instance:str
    x:str
    parameter:str
    def __init__(self, celex:str):
        self.celex = celex
        self.instance = Analyzer(self.celex)
        self.x = self.instance()

      

    def to_csv(self):
        file=open("csv/output.csv","a+")
        writer=csv.writer(file)
       
        if self.x!=None:
            writer.writerow([self.celex,self.x])
        
    def to_json(self):
        if self.x!=None:
            data={'Celex':self.celex,"Operative part":self.x}
            file=open('json/data.json', 'a+')
            json.dump(data,file)
            file.close()
    def to_txt(self):
      
     
        if self.x!=None:
            file=open(f"txt/{self.celex}.txt","a")
            for w in self.x:
                
                file.write(w+"\n")
            file.close()
#Sample code for reading celex id's froma tsv file

file=open("gijs_202310_node_list.tsv","r")
reader=csv.reader(file)
from output import Writing
testing=[]
for row in reader:
    for rows in row:
        if "Id" not in rows:
            testing.append(rows.split("\t")[0])
for all in testing:
    instance=Writing(all)
    instance.to_csv()
    print(all)                        


