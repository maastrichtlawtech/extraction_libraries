# Cellar extractor

This library contains two functions to get cellar case law data from eurlex.

## Version

Python 3.9+

## Tests

![Workflow Status](https://github.com/maastrichtlawtech/extraction_libraries/actions/workflows/github-actions.yml/badge.svg)

## Contributors

<table>
   <tr>
      <td align="center"> <a href="https://github.com/pranavnbapat"> <img src="https://avatars.githubusercontent.com/u/7271334?v=4" width="100;" alt="pranavnbapat"/> <br />
         <sub><b>Pranav Bapat</b></sub> </a> 
      </td>
      <td align="center"> <a href="https://github.com/Cloud956"> <img src="https://avatars.githubusercontent.com/u/24865274?v=4" width="100;" alt="Cloud956"/> <br /> <sub><b>Piotr Lewandowski</b></sub> </a> </td>
      <td align="center"> <a href="https://github.com/shashankmc"> <img src="https://avatars.githubusercontent.com/u/3445114?v=4" width="100;" alt="shashankmc"/> <br /> <sub><b>shashankmc</b></sub> </a> </td>
      <td align="center"> <a href="https://github.com/gijsvd"> <img src="https://avatars.githubusercontent.com/u/31765316?v=4" width="100;" alt="gijsvd"/> <br /> <sub><b>gijsvd</b></sub> </a> </td>
      <td align="center"> <a href="https://github.com/venvis"> <img src="https://avatars.githubusercontent.com/venvis" width="100;" alt="venvis"/> <br /> <sub><b>venvis</b></sub> </a> </td>
   </tr>
</table>

## How to install?

``pip install cellar-extractor``

## What are the functions?

1. ``get_cellar``  
    Gets all the ECLI data from the eurlex sparql endpoint and saves them in the CSV or JSON format, in-memory or as a saved file.
2. ``get_cellar_extra``  
    Gets all the ECLI data from the eurlex sparql endpoint, and on top of that scrapes the eurlex websites to acquire 
    the full text, keywords, case law directory code and eurovoc identifiers. If the user does have an eurlex account with access to the eurlex webservices, he can also 
    pass his webservices login credentials to the method, in order to extract data about works citing work and works 
    being cited by work. The full text is returned as a JSON file, rest of data as a CSV.  Can be in-memory or as saved files.
3. ``get_nodes_and_edges_lists``  
    Gets 2 list objects, one for the nodes and edges of the citations within the passed dataframe.
    Allows the creation of a network graph of the citations. Can only be returned in-memory.
4. ``filter_subject_matter``  
    Returns a dataframe of cases only containing a certain phrase in the column containing the subject of cases.

## What are the classes?

1. ``FetchOperativePart``  
    A class whose instance(declaration) when called returns a list of the all the text contained within the operative part for each European Court of Justice (CJEU, formerly known as European Court of Justice (ECJ)) judgement (English only).  The ``FetchOperativePart`` class has eleven functions - each function scrapes for the operative part depending on the html structure of the page :
    - ``html_page_structure_one`` -  This function retreives operative part from documents of the respected celex id's. This function scrapes/parse the operative part from a nested table structure . The relevant text lies inside the coj-bold class of the span tag.
    - ``html_page_structure_two`` - This function retreives operative part from documents of the respected celex id's. This function scrapes/parse the operative part from a paragraph (p) structure. The relevant text lies inside the normal class of the p tag which comes after the keyword operative of the previous span tag.
    - ``structure_three`` - This function retreives operative part from documents of the respected celex id's. This function scrapes/parse the operative part from a nested table structure. The relevant text lies inside the coj-bold class of the span tag.
    - `structure_four` - This function retrieves the operative part from documents of the respected celex ids. This function scrapes/parses the operative part from a paragraph (p) structure. The relevant text lies inside the p tag which comes after the keyword operative of the previous span tag.
    - `structure_five` - This function retrieves the operative part from documents of the respected celex ids. This function scrapes/parses the operative part from a paragraph (p) structure. The relevant text lies inside the normal class of the p tag which comes after the keyword operative of the previous span tag.
    - `structure_six` - This function retrieves the operative part from documents of the respected celex ids. This function scrapes/parses the operative part from a h2 (header) structure. The relevant text lies inside the p tag which comes after the keyword operative part of the respective h2 tag.
    - `structure_seven` - This function retrieves the operative part from documents of the respected celex ids. This function scrapes/parses the operative part from a table (table) structure. The relevant text lies inside the span tag which comes after the p tag, with the class name=normal. 
    - `structure_eight` - This function retrieves the operative part from documents of the respected celex ids. The text is extracted from the span tag nested inside the tbody tag. Returns a list as output.
    - `structure_nine` - This function retrieves the operative part from documents of the respected celex ids. The operative part is under the bold (b) tag after the p tag where the keywords "on those grounds" exist.
    - `structure_ten` - This function retrieves the operative part from documents of the respected celex ids. Since the content is preloaded using js/client server side functions, the text from the current page is retrieved and the operative part is scraped after the occurrence of the phrase "On those grounds".
    - `structure_eleven` - This function retrieves the operative part from documents of the respected celex ids. The operative part is under the paragraph (p) tag after the b tag where the keywords "operative part" exist.

2. ``Writing``  
A class which writes the text for the operative part for each European Case law case(En-English only) into csv,json and txt files(Generated upon initialization). The ``Writing`` class has three functions:
    - ``to_csv()`` - Writes the operative part along with celex id into a csv file.
    - ``to_json()`` - Writes the operative part along with celex id into a json file.
    - ``to_txt()`` - Writes the operative part along with celex id into a txt file
   
3. ``CellarSparqlQuery``
A class which includes methods to extract extra data for each court case using a sparql query.
      - ``get_endorsements`` - Fetches endorsements of the judgement
      - ``get_subjects`` - Fetches subjects of the judgement
      - ``get_parties`` - Fetches parties of the judgement
      - ``get_keywords`` - Fetches keywords of the judgement
      - ``get_citations`` - Fetches court cases cited by the source judgement
      - ``get_grounds`` - Fetches grounds of the judgement

## What are the parameters?

1. ``get_cellar``  
    **Parameters**:
    - **max_ecli**: **int, optional, default 100**  
    Maximum number of ECLIs to retrieve.
    - **sd: date, optional, default '2022-05-01'**  
    The start last modification date (yyyy-mm-dd).
    - **ed: date, optional, default current date**  
    The end last modification date (yyyy-mm-dd).
    - **save_file: ['y', 'n'],optional, default 'y'**  
    Save data in a data folder, or return in-memory.
    - **file_format: ['csv', 'json'],optional, default 'csv'**  
    Returns the data as a JSON/dictionary, or as a CSV/Pandas Dataframe object.

2. ``get_cellar_extra``
    - **max_ecli: int, optional, default 100**  
    Maximum number of ECLIs to retrieve.
    - **sd: date, optional, default '2022-05-01'**  
    The start last modification date (yyyy-mm-dd).
    - **ed: date, optional, default current date**  
    The end last modification date (yyyy-mm-dd).
    - **save_file: ['y', 'n'],optional, default 'y'**  
    Save the full text of cases as JSON file / return as a dictionary and save the rest ofthe data as a CSV file / return as a Pandas Dataframe object.
    - **threads: int ,optional, default 10**  
    Extracting the additional data takes a lot of time. The use of multi-threading can cut down this time. Even with this, the method may take a couple of minutes for a couple of hundred cases. A maximum number of 10 recommended, as this method may also affect the device's internet connection.
    - **username: string, optional, default empty string**  
    The username to the eurlex webservices.
    - **password: string, optional, default empty string**  
    The password to the eurlex webservices.

3. ``get_nodes_and_edges_lists``
    - **df: DataFrame object, required, default None**  
    DataFrame of cellar metadata acquired from the ``get_cellar_extra`` method with eurlex webservice credentials passed. This method will only work on dataframes with citations data.
    - **only_local: boolean, optional, default False**  
    Flag for nodes and edges generation. If set to True, the network created will only include nodes and edges between
    cases exclusively inside the given dataframe.

4. ``filter_subject_matter``
    - **df: DataFrame object, required, default None**  
    DataFrame of cellar metadata acquired from any of the cellar extraction methods listed above.
    - **phrase: string, required, default None**  
    The phrase which has to be present in the subject matter of cases. Case insensitive.

5. ``Analyzer``
    - **celex id: str, required**
        - Pass as a constructor upon initializing the class

6. ``Writing``
    - **celex id: str, required**
        - Pass as a constructor upon initializing the class

## Examples

```python
import cellar_extractor as cell

# Below are examples for in-file saving:

cell.get_cellar(save_file='y', max_ecli=200, sd='2022-01-01', file_format='csv')
cell.get_cellar_extra(max_ecli=100, sd='2022-01-01', threads=10)

# Below are examples for in-memory saving:

df = cell.get_cellar(save_file='n', file_format='csv', sd='2022-01-01', max_ecli=1000)
df,json = cell.get_cellar_extra(save_file='n', max_ecli=100, sd='2022-01-01', threads=10)
```

Create a callback of the instance of the class initiated and pass a list as it's value.

```python
import cellar_extractor as cell
instance=cell.FetchOperativePart(celex_id:str)
output_list=instance()
print(output_list) # prints operative part of the Case as a list
```

The Writing Class also takes a celex id , upon initializing the class , through the means of the constructor and writes the content of its operative part into different files, depending on the function called.

```python
import cellar_extractor as cell
instance=cell.Writing(celex_id:str)
output=instance.to_csv() # for csv
output=instance.to_txt() # for txt
output=instance.to_json() # for json
```

## License
[![License: Apache 2.0](https://img.shields.io/github/license/maastrichtlawtech/extraction_libraries)](https://opensource.org/licenses/Apache-2.0)

Previously under the [MIT License](https://opensource.org/licenses/MIT), as of 28/10/2022 this work is licensed under a [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0).
```
Apache License, Version 2.0

Copyright (c) 2022 Maastricht Law & Tech Lab

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
