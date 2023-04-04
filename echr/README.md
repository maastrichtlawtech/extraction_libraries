## echr extractor
This library contains functions to get ECHR data.

## Version
Python 3.9

## Contributors

<!-- readme: contributors,gijsvd -start -->
<table>
<tr>
    <td align="center">
        <a href="https://github.com/brodriguesdemiranda">
            <img src="https://avatars.githubusercontent.com/u/35369949?v=4" width="100;" alt="brodriguesdemiranda"/>
            <br />
            <sub><b>Benjamin Rodrigues de Miranda</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/ChloeCro">
            <img src="https://avatars.githubusercontent.com/u/99276050?v=4" width="100;" alt="ChloeCro"/>
            <br />
            <sub><b>Chloe Crombach</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/Cloud956">
            <img src="https://avatars.githubusercontent.com/u/24865274?v=4" width="100;" alt="Cloud956"/>
            <br />
            <sub><b>Piotr Lewandowski</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/pranavnbapat">
            <img src="https://avatars.githubusercontent.com/u/7271334?v=4" width="100;" alt="pranavnbapat"/>
            <br />
            <sub><b>Pranav Bapat</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/running-machin">
            <img src="https://avatars.githubusercontent.com/u/60750154?v=4" width="100;" alt="running-machin"/>
            <br />
            <sub><b>running-machin</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/shashankmc">
            <img src="https://avatars.githubusercontent.com/u/3445114?v=4" width="100;" alt="shashankmc"/>
            <br />
            <sub><b>shashankmc</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/gijsvd">
            <img src="https://avatars.githubusercontent.com/u/31765316?v=4" width="100;" alt="gijsvd"/>
            <br />
            <sub><b>gijsvd</b></sub>
        </a>
    </td>
</tr>
</table>
<!-- readme: contributors,gijsvd -end -->

## How to install?
<code>pip install echr-extractor</code>

## What are the functions?
<ol>
    <li><code>get_echr</code></li>
     Gets all of the available metadata for echr cases from the HUDOC database.
    Can be saved in a file or returned in-memory.
<br>
    <li><code>get_echr_extra</code></li>
    Gets all of the available metadata for echr cases from the HUDOC database. 
On top of that downloads the full text for each case downloaded. Can be saved in a file or returned in-memory.
<br>
    <li><code>get_nodes_edges</code></li>
    Gets all of the available nodes and edges for echr cases for given metadata from the HUDOC database.
</ol>

## What are the parameters?
<ol>
    <li><code>get_echr</code></li> 
    <ul>
        <li><strong>start_id: int, optional, default: 0</strong></li>
        The id of the first case to be downloaded.
         <li><strong>end_id: int, optional, default: The maximum number of cases available</strong></li>
        The id of the last case to be downloaded.
        <li><strong>count: int, optional, default: None </strong></li>
        The number of cases per language to be downloaded, starting from the start_id. 
        <br><strong>!NOTICE!</strong><br>
        If count is provided, the end_id will be set to start_id+count, overwriting any given end_id value.
        <li><strong>start_date: date, optional, default None</strong></li>
        The start publication date (yyyy-mm-dd)
        <li><strong>end_date: date, optional, default current date</strong></li>
        The end publication date (yyyy-mm-dd)
        <li><strong>verbose: boolean, optional, default False</strong></li>
        This option allows for additional printing, showing live progress of the extraction process.
        <li><strong>skip_missing_dates: boolean, optional, default False</strong></li>
        This option makes the extraction not collect data for cases where there is no judgement date provided.
        <li><strong>fields: list of strings, optional, default all available fields</strong></li>
        This argument can be provided, to limit the metadata to be downloaded. These fields will appear as 
        different columns in the csv file / Dataframe object. The full list of fields is attached in the appendix.
        <li><strong>save_file: ['y', 'n'],optional, default 'y'</strong></li>
        Save metadata as a csv file in the data folder, or return as a Pandas DataFrame object in-memory.
        <li><strong>link: string ,optional, default None </strong></li>
        Allows the user to download results of a search from the HUDOC website. If this argument is provided, all
        the other arguments are ignored, except for 'fields'. Further information on proper usage is in the Appendix.
        <li><strong>language: list of strings, optional, default ['ENG']</strong></li>
        The language of the metadata to be downloaded from the available languages.
        <br><strong>!NOTICE!</strong><br>
        If link is provided, the language argument will not be used, as the language also appears in the link.
</ul>
    <li><code>get_echr_extra</code></li>
    <ul> 
        <li><strong>start_id: int, optional, default: 0</strong></li>
        The id of the first case to be downloaded.
        <li><strong>end_id: int, optional, default: The maximum number of cases available</strong></li>
        The id of the last case to be downloaded.
        <li><strong>count: int, optional, default: None </strong></li>
        The number of cases per language given as input to be downloaded, starting from the start_id. 
        <br><strong>!NOTICE!</strong><br>
        If count is provided, the end_id will be set to start_id+count, overwriting any given end_id value.
        <li><strong>start_date: date, optional, default None</strong></li>
        The start publication date (yyyy-mm-dd)
        <li><strong>end_date: date, optional, default current date</strong></li>
        The end publication date (yyyy-mm-dd)
        <li><strong>verbose: boolean, optional, default False</strong></li>
        This option allows for additional printing, showing live progress of the extraction process.
        <li><strong>skip_missing_dates: boolean, optional, default False</strong></li>
        This option makes the extraction not collect data for cases where there is no judgement date provided.
        <li><strong>fields: list of strings, optional, default all available fields</strong></li>
        This argument can be provided, to limit the metadata to be downloaded. These fields will appear as 
        different columns in the csv file / Dataframe object. The full list of fields is attached in the appendix.
        <li><strong>save_file: ['y', 'n'],optional, default 'y'</strong></li>
        Save metadata as a csv file in the data folder and the full_text as a json file, 
        or return a Pandas DataFrame object and a list of dictionaries in-memory.
        <li><strong>language: list of strings, optional, default ['ENG']</strong></li>
        The language of the metadata to be downloaded from the available languages.
        <br><strong>!NOTICE!</strong><br>
        If link is provided, the language argument will not be used, as the language also appears in the link.
        <li><strong>link: string ,optional, default None </strong></li>
        Allows the user to download results of a search from the HUDOC website. If this argument is provided, all
        the other arguments are ignored, except for 'fields'. Further information on proper usage is in the Appendix.
        <li><strong>threads: int, optional, default: 10</strong></li>
        The full text download is a parallelizable process.
        This parameter determines the number of threads to be used in the download.
    </ul>
    <li><code>get_nodes_edges</code></li>
    <ul>
        <li><strong>metadata_path</strong></li>
        The path to the metadata file to read.
        <li><strong>save_file: ['y', 'n'],optional, default 'y'</strong></li>
        Save the nodes and edges of cases in metadata as csv files in the data folder, or return them as Pandas Dataframe objects in-memory.
    </ul>
</ol>

## Examples

```
import echr_extractor as echr

Below are examples for in-file saving:

df, json = echr.get_echr_extra(count=100,save_file='y',threads=10)
df = echr.get_echr(start_id=1,save_file='y',skip_missing_dates=True)

Below are examples for in-memory saving:

df, json = echr.get_echr_extra(start_id=20,end_id=3000,save_file='n')
    
df = echr.get_echr(start_id=1000,count=2000,save_file='n',verbose=True)

nodes, edges = echr.get_nodes_edges(metadata_path='data/echr_metadata.csv',save_file='n')
```
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


## Appendix

```
To properly use the 'link' parameter of the extraction methods, the user should head to 

https://hudoc.echr.coe.int/eng#%20

There, the user can use the tools of Advanced Search of HUDOC to search for specific cases.
Afterwards*, the user can copy the link of the current website, and pass it on to the extraction methods. 


* It should be noted that the link only updates after the 'search' button  of the Advanced Search is clicked.



The full list of fields is as follows:

fields = ['itemid','applicability','application','appno','article','conclusion','decisiondate','docname',
'documentcollectionid','documentcollectionid2','doctype','doctypebranch','ecli','externalsources','extractedappno',
'importance','introductiondate','isplaceholder','issue','judgementdate','kpdate','kpdateAsText','kpthesaurus',
'languageisocode','meetingnumber','originatingbody','publishedby','Rank','referencedate','reportdate','representedby',
'resolutiondate',resolutionnumber','respondent','respondentOrderEng','rulesofcourt','separateopinion','scl',
'sharepointid','typedescription','nonviolation','violation']

```
These fields can take different values, for more information head to https://hudoc.echr.coe.int.