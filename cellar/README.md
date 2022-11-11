## Cellar extractor
This library contains two functions to get cellar case law data from eurlex.

## Version
Python 3.9

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
<code>pip install cellar-extractor</code>

## What are the functions?
<ol>
    <li><code>get_cellar</code></li>
    Gets all the ECLI data from the eurlex sparql endpoint and saves them in the CSV or JSON format, in-memory or as a saved file.
    <br>
    <li><code>get_cellar_extra</code></li>
    Gets all the ECLI data from the eurlex sparql endpoint, and on top of that scrapes the eurlex websites to acquire 
    the full text, keywords, case law directory code and eurovoc identifiers. The full text is returned as a JSON file,
    rest of data as a CSV. Can be in-memory or as saved files.
</ol>

## What are the parameters?
<ol>
    <li><code>get_cellar</code></li>
    <strong>Parameters:</strong>
    <ul>
        <li><strong>max_ecli: int, optional</strong></li>
        Maximum amount of ECLIs to retrieve
        <br>Default: 100
        <li><strong>sd: date, optional, default '2022-05-01'</strong></li>
        The start publication date (yyyy-mm-dd)
        <li><strong>ed: date, optional, default current date</strong></li>
        The end publication date (yyyy-mm-dd)
        <li><strong>save_file: ['y', 'n'],optional, default 'y'</strong></li>
        Save data as in a data folder, or return in-memory
        <li><strong>file_format: ['csv', 'json'],optional, default 'csv'</strong></li>
        Returns the data as a JSON/dictionary, or a CSV/Pandas Dataframe object.
    </ul>
    <li><code>get_cellar_extra</code></li>
    <ul> ed=None, save_file='y', max_ecli=100, sd="2022-05-01",threads=10
        <li><strong>max_ecli: int, optional</strong></li>
        Maximum amount of ECLIs to retrieve
        <br>Default: 100
        <li><strong>sd: date, optional, default '2022-05-01'</strong></li>
        The start publication date (yyyy-mm-dd)
        <li><strong>ed: date, optional, default current date</strong></li>
        The end publication date (yyyy-mm-dd)
        <li><strong>save_file: ['y', 'n'],optional, default 'y'</strong></li>
        Save the full text of cases as JSON file / return as a dictionary and save the rest of
        the data as a CSV file / return as a Pandas Dataframe object
        <li><strong>threads: int ,optional, default 10</strong></li>
        Extracting the additional data takes a lot of time. The use of multi-threading can cut down this time.
        Even with this, the method may take a couple of minutes for a couple of hundred cases. A maximum number
        of 15 recommended, as this method may also affect the devices internet connection.
        <br>Default: 100
    </ul>
</ol>


## Examples
```
import cellar_extractor as cell

Below are examples for in-file saving:

cell.get_cellar(save_file='y', max_ecli=200, sd='2022-01-01', file_format='csv')
cell.get_cellar_extra(max_ecli=100, sd='2022-01-01', threads=15)

Below are examples for in-memory saving:

df = cell.get_cellar(save_file='n', file_format='csv', sd='2022-01-01', max_ecli=1000)
df,json = cell.get_cellar_extra(save_file='n', max_ecli=100, sd='2022-01-01', threads=15)
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
