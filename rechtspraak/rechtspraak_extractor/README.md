## Rechtspraak extractor
This library contains two functions to get rechtspraak data and metadata from the API.

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
            <img src="https://avatars.githubusercontent.com/u/24865274?v=4" width="100;" alt="pranavnbapat"/>
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
<ol>
    <li>get_rechtspraak</li>
    Gets all the ECLIs and saves them in the CSV file or in-memory.
    <br>It gets, ECLI, title, summary, updated date, link.
    <li>get_rechtspraak_metadata</li>
    Gets the metadata of the ECLIs created by above function and saves them in the new CSV file or in-memory.
    <br>Link attribute that we get from the above function contains the links of ECLI metadata.
    <br>It gets instantie, datum uitspraak, datum publicatie, zaaknummer, rechtsgebieden, bijzondere kenmerken, 
    inhoudsindicatie, and vindplaatsen
</ol>

## What are the parameters?
<ol>
    <li><strong>get_rechtspraak(max_ecli=100, sd='2022-05-01'), ed='2022-10-01', save_file='y')</strong></li>
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
        Save data as a CSV file in data folder
    </ul>
    <li>get_rechtspraak_metadata</li>
    <ul>
        <li><strong>save_file: ['y', 'n'], default 'y'</strong></li>
        <li><strong>dataframe: dataframe, optional</strong></li>
        Dataframe containing ECLIs to retrieve metadata. Cannot be combined with filename
        <li><strong>filename: string, optional</strong></li>
        CSV file containing ECLIs to retrieve metadata. Cannot be combined with dataframe
    </ul>
</ol>

## Examples
<code>
import rechtspraak_extractor as rex<br><br>
rex.get_rechtspraak(max_ecli=1000, sd='2022-08-01', save_file='y')<br><br>
rex.get_rechtspraak_metadata(save_file='y', filename='rechtspraak.csv')<br><br>
If you want in-memory data, and not in a CSV file, assign it to a variable and that variable will contain the dataframe
<br>
df = rex.get_rechtspraak_metadata(save_file='n')
df_metadata = rex.get_rechtspraak_metadata(save_file='n', dataframe=df)
</code>


## License
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Previously under the [Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/legalcode.en)), as of 13/02/2022 this work is licensed under a [MIT License](https://opensource.org/licenses/MIT).
```
MIT License

Copyright (c) 2022 Maastricht Law & Tech Lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```