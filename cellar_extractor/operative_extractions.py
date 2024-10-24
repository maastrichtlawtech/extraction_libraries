import csv
import json
import os
import requests
from bs4 import BeautifulSoup
from SPARQLWrapper import JSON, SPARQLWrapper


class FetchOperativePart:
    """
    This class returns a list of the operative part for a given celex id.
    Celex id is initialized through a constructor.
    """

    celex: str = ""  # declare celex as a string
    # declare url as a string
    url: str = ""

    def __init__(self, celex):
        # Initialize Celex id as a constructor, passed when calling the class
        self.celex = celex
        self.url = f"https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A{self.celex}&from=EN"
        self.sparql = SPARQLWrapper("https://publications.europa.eu/webapi/rdf/sparql")

    def get_operative_sparql(self) -> str:
        """
        Attempts to get the operative part using SPARQL query.
        Returns None if query fails or returns no results.
        """
        try:
            self.sparql.setReturnFormat(JSON)
            self.sparql.setQuery(
                """
            PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?operative
            WHERE { 
                ?doc cdm:manifestation_case-law_operative_part ?operative ;
                     owl:sameAs ?w .
                FILTER (?w = <http://publications.europa.eu/resource/celex/%s.ENG.txt>)
            }
            """
                % self.celex
            )

            ret = self.sparql.queryAndConvert()

            if ret["results"]["bindings"]:
                operative = ret["results"]["bindings"][0]["operative"]["value"]
                parser = BeautifulSoup(operative.strip(), "html.parser")
                return parser.text
            return None

        except Exception:
            return None

    def html_page_structure_one(self) -> list:
        """
        This function retreives operative part from documents
        of the respected celex id's.
        This function scrapes/parse the operative part from a nested
        table structure . The relevant text lies inside the coj-bold
        class of the span tag.
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")
        div = parser.find_all("table")  # Find all tables tag from the website
        one = []
        for divs in div:
            # Find each nested table within the table
            table = divs.find("table")
            if table is not None:
                # Find all p under the nested table with the coj-normal class
                p = table.find_all("p", class_="coj-normal")
                for x in p:
                    # Span class of coj-bold under the p tag
                    span = x.find_all("span", class_="coj-bold")
                    for y in span:
                        if x is not None and y is not None:
                            # append text from span onto a list
                            one.append(y.text)
        return one

    def html_page_structure_two(self) -> list:
        """
        This function retreives operative part from documents
        of the respected celex id's.
        This function scrapes/parse the operative part from a paragraph
        (p) structure . The relevant text lies inside the
        normal class of the p tag which
        comes after the keyword operative of the previous span tag.
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")
        p = parser.find_all("p")
        two = []
        for para in p:
            span = para.find("span")
            if span is not None:
                if "operative" in span.text.lower():
                    normal = span.find_all_next("p", class_="normal")
                    for op in normal:
                        two.append(op.text)
        return two

    def structure_three(self) -> list:
        """
        This function retreives operative part from documents of the
        respected celex id's.
        This function scrapes/parse the operative part from a nested
        table structure. The relevant text lies inside the coj-bold class
        of the span tag.
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")
        table = parser.find_all("table")
        three = []
        for tables in table:
            interior = tables.find_all("table")
            for interiors in interior:
                if interiors is not None:
                    p = interiors.find_all("p", class_="coj-normal")
                    for x in p:
                        span = x.find_all("span", class_="coj-bold")
                        for y in span:
                            if x is not None and y is not None:
                                three.append(y.text)
        return three

    def structure_four(self) -> list:
        """
        This function retreives operative part from
        documents of the respected celex id's.
        This function scrapes/parse the operative part from a paragraph
        (p) structure . The relevant text lies inside the p  tag which
        comes after the
        keyword operative of the previous span tag.
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")
        p = parser.find_all("p")
        four = []
        for para in p:
            span = para.find("span")
            if span is not None:
                if "operative" in span.text.lower():
                    normal = span.find_all_next("table")
                    for op in normal:
                        tbody = op.find("tbody")
                        new_p = tbody.find_all("p", class_="oj-normal")
                        for subsequent in new_p:
                            if subsequent is not None:
                                four.append(subsequent.text)
        return four

    def structure_five(self) -> list:
        """
        This function retreives operative part from documents
        of the respected celex id's.
        This function scrapes/parse the operative part from a paragraph
        (p) structure. The relevant text lies inside the normal
        class of the p tag which
        comes after the keyword operative of the previous span tag.
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")
        p = parser.find_all("p")
        five = []
        for para in p:

            span = para.find("span")
            if span is not None:
                if "operative" in span.text.lower():
                    normal = span.find_all_next("table")
                    for op in normal:
                        tbody = op.find("tbody")
                        new_p = tbody.find_all("p", class_="normal")
                        for subsequent in new_p:
                            if subsequent is not None:
                                five.append(subsequent.text)

        return five

    def structure_six(self) -> list:
        """
        This function retreives operative part from documents of the
        respected celex id's.
        This function scrapes/parse the operative part from a h2 (header)
        structure.
        The relevant text lies inside thee p tag which comes after the keyword
        operative
        part of the respective h2  tag.
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")
        div = parser.find_all("h2")
        six = []
        for h2 in div:
            # print(h2.text)
            if h2.text == "Operative part":
                operatives = h2.find_all_next("p")
                for operative in operatives:

                    six.append(operative.text)
        return six

    def structure_seven(self) -> list:
        """
        This function retreives operative part from documents of the
        respected celex id's.
        This function scrapes/parse the operative part from a table
        (table) structure. The relevant text lies inside the span tag
        which comes after
        the p tag , with the class name=normal.
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")
        div = parser.find_all("table")
        seven = []
        for divs in div:
            # find tbody within the table
            table = divs.find_all("tbody")
            for tables in table:
                if tables is not None:
                    # find tr within the tbody
                    p = tables.find_all("tr")
                    for x in p:
                        if x is not None:
                            # find td within the tr
                            td = x.find_all("td")
                            for y in td:
                                if y is not None:
                                    p = y.find_all("p", class_="normal")
                                    for _all in p:
                                        if _all is not None:
                                            # find operative part
                                            # within the span
                                            span = _all.find_all("span",
                                                                 class_="bold")
                                            for spans in span:
                                                # Append it into a list and
                                                # return the
                                                # list when the function is
                                                # called
                                                seven.append(spans.text)
        return seven

    def structure_eight(self) -> list:
        """
        This function retreives operative part from
        documents of the respected celex id's.
        The text is extracted from the span tag nested inside
        the tbody tag.Returns a list as output.
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")

        tbody = parser.find_all("tbody")
        eight = []
        for _all in tbody:
            if _all is not None:
                tr = _all.find_all("tr")
                for trs in tr:
                    if trs is not None:
                        p = parser.find_all("p", class_="normal")
                        for paras in p:
                            if paras is not None:
                                if "on those grounds" in paras.text.lower():
                                    span = paras.find_all_next("span",
                                                               class_="bold")
                                    for spans in span:
                                        if spans is not None:
                                            eight.append(spans.text)
        return eight

    def structure_nine(self) -> list:
        """
        This function retreives operative part from documents of
        the respected celex id's.
        The operative part is under the bold(b)
        tag after the p tag where the keywords "on those grounds" exist.
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")
        nine = []
        div = parser.find_all("p")
        for divs in div:
            if divs is not None:
                if "on those grounds" in divs.text.lower():
                    b = divs.find_all_next("b")
                    for bolds in b:
                        nine.append(bolds.text)
        return nine

    def structure_eleven(self) -> list:
        """
        This function retreives operative part from documents
        of the respected celex id's.
        The operative part is under the paragraph(p)
        tag after the b tag where the keywords "operative part" exist.
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")
        bold = parser.find_all("b")

        eleven = []

        for b in bold:
            if b is not None:
                if "operative part" in b.text.lower():
                    tables = b.find_all_next("p")
                    for table in tables:
                        if table is not None:
                            eleven.append(table.text)
        return eleven

    def structure_ten(self):
        """
        This function retreives operative part from documents
        of the respected celex id's.
        Since the ocntent is preloaded using js/clients
        server side functions , the text from the current
        page is retrieved and the
        operative part is scraped after the occurence of the phrase
        "On those grounds".
        """
        website = requests.get(self.url, timeout=60).text
        parser = BeautifulSoup(website, "html.parser")
        appender = []
        for string in parser.stripped_strings:

            appender.append(string)

        found = False
        after_grounds = []

        for x in appender:

            if "on those grounds" in x.lower():
                found = True

            if found:
                if len(x.split(" ")) > 3:
                    after_grounds.append(x)
        return after_grounds

    def __call__(self) -> list:
        """
        This inbuilt __call__ function loops through
        all the methods in the class
        `Analyzer` and returns  the list , with values of the operative part .
        """

        sparql_result = self.get_operative_sparql()
        if sparql_result:
            return [sparql_result]

        container = [
            self.html_page_structure_one(),
            self.html_page_structure_two(),
            self.structure_three(),
            self.structure_four(),
            self.structure_five(),
            self.structure_six(),
            self.structure_seven(),
            self.structure_eight(),
            self.structure_nine(),
            self.structure_ten(),
            self.structure_eleven(),
        ]

        for result in container:
            if result and (len(result) != 0 and result[0] != "\n"):
                return result

        return []


class Writing:
    """
    This class has different methods, for the purpose
    of writing the operative part
    into different file formats.(Csv,txt,json)
    """

    instance: str
    x: str
    parameter: str

    current_dir = os.getcwd()

    txt_dir = os.path.join(current_dir, "txt")
    csv_dir = os.path.join(current_dir, "csv")
    json_dir = os.path.join(current_dir, "json")

    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    def __init__(self, celex: str):
        self.celex = celex
        self.instance = FetchOperativePart(self.celex)
        self.x = self.instance()

    def to_csv(self):
        _file = open("csv/output.csv", "a+", encoding="utf-8")
        writer = csv.writer(_file)
        if self.x is not None:
            writer.writerow([self.celex, self.x])

    def to_json(self):
        if self.x is not None:
            data = {"Celex": self.celex, "Operative part": self.x}
            _file = open("json/data.json", "a+", encoding="utf-8")
            json.dump(data, _file)
            _file.close()

    def to_txt(self):
        if self.x is not None:
            _file = open(f"txt/{self.celex}.txt", "a", encoding="utf-8")
            for w in self.x:
                _file.write(w + "\n")
            _file.close()
