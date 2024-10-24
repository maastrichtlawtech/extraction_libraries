from SPARQLWrapper import JSON, SPARQLWrapper
from bs4 import BeautifulSoup


class CellarSparqlQuery:

    def __init__(self):
        # Set the SPARQL endpoint
        _url = "https://publications.europa.eu/webapi/rdf/sparql"
        self.sparql = SPARQLWrapper(_url)
        self.sparql.setReturnFormat(JSON)

    def get_endorsements(self, number):
        """
        Retrieves endorsements for a given document number from a SPARQL
        endpoint.
        Args:
            number (str): The document number to query endorsements for.
        Returns:
            str: A string containing the endorsements text, parsed from HTML.
        """

        self.sparql.setQuery(
            f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?Endorsements
        WHERE {{
            ?doc cdm:manifestation_case-law_endorsements ?Endorsements ;
                owl:sameAs ?w .
            FILTER (?w = <http://publications.europa.eu/resource/celex/{number}.ENG.txt>)
        }}
        LIMIT 100
        """
        )

        ret = self.sparql.queryAndConvert()
        print(ret)
        endorsements = ""
        for result in ret["results"]["bindings"]:
            endorsements += result["Endorsements"]["value"]

        return BeautifulSoup(endorsements, "html.parser").text

    def get_grounds(self, number):
        """
        Retrieves the grounds of a case-law document based on its CELEX number.
        Args:
            number (str): The CELEX number of the case-law document.
        Returns:
            str: The grounds of the case-law document as plain text.
        """
        self.sparql.setQuery(
            f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?Grounds
        WHERE {{
            ?wc cdm:manifestation_case-law_grounds ?Grounds ;
                owl:sameAs ?w .
            FILTER (?w = <http://publications.europa.eu/resource/celex/{number}.ENG.txt>)
        }}
        LIMIT 100
        """
        )

        ret = self.sparql.queryAndConvert()

        grounds = ""
        for result in ret["results"]["bindings"]:
            grounds += result["Grounds"]["value"]

        return BeautifulSoup(grounds, "html.parser").text

    def get_keywords(self, number):
        """
        Retrieves keywords for a given CELEX number from the EU Publications
        SPARQL endpoint.
        Args:
            number (str): The CELEX number of the document to retrieve
            keywords for.
        Returns:
            str: A string containing the keywords associated with the given
            CELEX number, parsed from HTML.
        Raises:
            Exception: If there is an issue with the SPARQL query or the
            endpoint.
        """
        self.sparql.setQuery(
            f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?Keywords
        WHERE {{
            ?wc cdm:manifestation_case-law_keywords ?Keywords ;
                owl:sameAs ?w .
            FILTER (?w = <http://publications.europa.eu/resource/celex/{number}.ENG.txt>)
        }}
        LIMIT 100
        """
        )

        ret = self.sparql.queryAndConvert()

        keywords = ""
        for result in ret["results"]["bindings"]:
            keywords += result["Keywords"]["value"]

        return BeautifulSoup(keywords, "html.parser").text

    def get_parties(self, number):
        """
        Retrieves the parties involved in a case-law document
        from the EU Publications Office SPARQL endpoint.

        Args:
            number (str): The CELEX number of the case-law document.

        Returns:
            str: A string containing the parties involved in the
            case-law document, with HTML tags removed.
        """

        self.sparql.setQuery(
            f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?Parties
        WHERE {{
            ?wc cdm:manifestation_case-law_parties ?Parties ;
                owl:sameAs ?w .
            FILTER (?w = <http://publications.europa.eu/resource/celex/{number}.ENG.txt>)
        }}
        LIMIT 100
        """
        )

        ret = self.sparql.queryAndConvert()
        parties = ""
        for result in ret["results"]["bindings"]:
            parties += result["Parties"]["value"]

        return BeautifulSoup(parties, "html.parser").text

    def get_subjects(self, number):
        """
        Retrieves the subjects associated with a given CELEX
        number from the SPARQL endpoint.

        Args:
            number (str): The CELEX number of the document to query.

        Returns:
            str: A string containing the subjects related to the
            given CELEX number, parsed from HTML.
        """
        self.sparql.setQuery(
            f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?Subjects
        WHERE {{
            ?wc cdm:manifestation_case-law_subject ?Subjects ;
                owl:sameAs ?w .
            FILTER (?w = <http://publications.europa.eu/resource/celex/{number}.ENG.txt>)
        }}
        LIMIT 100
        """
        )

        ret = self.sparql.queryAndConvert()

        subjects = ""
        for result in ret["results"]["bindings"]:
            subjects += result["Subjects"]["value"]

        return BeautifulSoup(subjects, "html.parser").text

    def get_citations(self, source_celex, cites_depth=1, cited_depth=1):
        """
        Gets all the citations one to X steps away. Hops can be specified
        as either the source document citing another (defined by `cites_depth`)
        or another document citing it (`cited_depth`). Any numbers higher than
        1 denote that new source document citing a document of its own.
        This specific implementation does not care about intermediate steps
        it simply finds anything X or fewer hops away without linking those
        together.
        """
        self.sparql.setQuery(
            """
            prefix cdm: <http://publications.europa.eu/ontology/cdm#>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT DISTINCT * WHERE
            {
            {
                SELECT ?name2 WHERE {
                    ?doc cdm:resource_legal_id_celex "%s"^^xsd:string .
                    ?doc cdm:work_cites_work{1,%i} ?cited .
                    ?cited cdm:resource_legal_id_celex ?name2 .
                }
            } UNION {
                SELECT ?name2 WHERE {
                    ?doc cdm:resource_legal_id_celex "%s"^^xsd:string .
                    ?cited cdm:work_cites_work{1,%i} ?doc .
                    ?cited cdm:resource_legal_id_celex ?name2 .
                }
            }
            }"""
            % (source_celex, cites_depth, source_celex, cited_depth)
        )
        ret = self.sparql.queryAndConvert()

        targets = set()
        for bind in ret["results"]["bindings"]:
            target = bind["name2"]["value"]
            targets.add(target)
        targets = list(set([el for el in list(targets)]))

        return targets
