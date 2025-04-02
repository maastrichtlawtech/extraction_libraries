## Rechtspraak extractor
This library contains two functions to get rechtspraak data and metadata from the API.

## Version
Python 3.9+

## Contributors

<!-- readme: contributors,gijsvd -start -->
<table>
<tr>
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
        <a href="https://github.com/Cloud956">
            <img src="https://avatars.githubusercontent.com/u/24865274?v=4" width="100;" alt="Cloud956"/>
            <br />
            <sub><b>Piotr Lewandowski</b></sub>
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
<code>pip install rechtspraak_extractor</code>

## What are the functions?
<li><b>Rechtspraak Extractor</b>
<ol>
    <li><code>get_rechtspraak</code></li>
    Gets all the ECLIs and saves them in the CSV file or in-memory.
    <br>It gets, ECLI, title, summary, updated date, link.
    <li><code>get_rechtspraak_metadata</code></li>
    Gets the metadata of the ECLIs created by above function and saves them in the new CSV file or in-memory.
    <br>Link attribute that we get from the above function contains the links of ECLI metadata.
    <br>It gets instantie, datum uitspraak, datum publicatie, zaaknummer, rechtsgebieden, bijzondere kenmerken, 
    inhoudsindicatie, and vindplaatsen
</ol> </li>

## What are the parameters?
<ol>
    <li><strong>get_rechtspraak(max_ecli=100, sd='2022-05-01', ed='2022-10-01', save_file='y')</strong></li>
    <strong>Parameters:</strong>
    <ul>
        <li><strong>max_ecli: int, optional</strong></li>
        Maximum amount of ECLIs to retrieve
        <br>Default: 100
        <li><strong>sd: date, optional, default '2022-08-01'</strong></li>
        The start publication date (yyyy-mm-dd)
        <li><strong>ed: date, optional, default current date</strong></li>
        The end publication date (yyyy-mm-dd)
        <li><strong>save_file: ['y', 'n'], default 'y'</strong></li>
        y - Save data as a CSV file in data folder
        <br>n - Save data as a dataframe in-memory
    </ul>
    <li><code>get_rechtspraak_metadata</code></li>
    <ul>
        <li><strong>save_file: ['y', 'n'], default 'y'</strong></li>
        y - Save data as a CSV file in data folder
        <br>n - Save data as a dataframe in-memory
        <li><strong>dataframe: dataframe, optional</strong></li>
        Dataframe containing ECLIs to retrieve metadata. Cannot be combined with filename
        <li><strong>filename: string, optional</strong></li>
        CSV file containing ECLIs to retrieve metadata. Cannot be combined with dataframe
    </ul>
</ol>


## Examples
```
import rechtspraak_extractor as rex

-----------------------------------------------------------------------------------------------------------------------

# For rechtspraak

# To get the rechtspraak data in a dataframe:
df = rex.get_rechtspraak(max_ecli=100, sd='2022-08-01', save_file='n')  # Gets 100 ECLIs from 1st August 2022

# To save rechtspraak data as a CSV file:
rex.get_rechtspraak(max_ecli=100, sd='2022-08-01', save_file='y') 

-----------------------------------------------------------------------------------------------------------------------

# For rechtspraak metadata

# To get metadata as a dataframe from rechtspraak data (as a dataframe):
df_metadata = rex.get_rechtspraak_metadata(save_file='n', dataframe=df)

# To get metadata as a dataframe from rechtspraak file (as a dataframe):
df_metadata = rex.get_rechtspraak_metadata(save_file='n', filename='rechtspraak.csv')

# To get metadata as a dataframe from rechtspraak data (saved as CSV file):
rex.get_rechtspraak_metadata(save_file='y', dataframe=df)

# To get metadata and save as a CSV file:
rex.get_rechtspraak_metadata(save_file='y', filename='rechtspraak.csv')

-----------------------------------------------------------------------------------------------------------------------

# filename='rechtspraak.csv' - filename.csv is a file from the data folder created by get_rechtspraak method
# dataframe=df - df is a dataframe created by get_rechtspraak method

# Will not get any metadata
df = rex.get_rechtspraak_metadata(save_file='n')

# Will get the metadata of all the files in the data folder
rex.get_rechtspraak_metadata(save_file='y')
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
