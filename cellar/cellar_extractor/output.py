
# from typing import Any
from operative_extractions import Analyzer
import csv
import json

class Writing():
    
    instance:str
    x:str
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
    def __call__(self):
        self.to_csv()
        # self.to_json()
        # self.to_txt()        

         

        

# example=Writing("62018CA0390")
# example()

