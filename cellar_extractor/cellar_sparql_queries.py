from SPARQLWrapper import JSON, SPARQLWrapper
from bs4 import BeautifulSoup

class CellarSparqlQuery:

    def get_endorsements(self,number):
        sparql = SPARQLWrapper('https://publications.europa.eu/webapi/rdf/sparql')
        sparql.setReturnFormat(JSON)
        
        sparql.setQuery(f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?Endorsements
        WHERE {{ 
            ?doc cdm:manifestation_case-law_endorsements ?Endorsements ;
                owl:sameAs ?w .
            FILTER (?w = <http://publications.europa.eu/resource/celex/{number}.ENG.txt>)
        }}
        LIMIT 100
        """)

        ret = sparql.queryAndConvert()

        endorsements = ""
        for result in ret['results']['bindings']:
            endorsements+=result['Endorsements']['value']

        return BeautifulSoup(endorsements,'html.parser').text
    
    def get_grounds(self,number):
        sparql = SPARQLWrapper('https://publications.europa.eu/webapi/rdf/sparql')
        sparql.setReturnFormat(JSON)
        
        sparql.setQuery(f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?Grounds
        WHERE {{ 
            ?wc cdm:manifestation_case-law_grounds ?Grounds ;
                owl:sameAs ?w .
            FILTER (?w = <http://publications.europa.eu/resource/celex/{number}.ENG.txt>)
        }}
        LIMIT 100
        """)

        ret = sparql.queryAndConvert()

        grounds = ""
        for result in ret['results']['bindings']:
            grounds+=result['Grounds']['value']

        return BeautifulSoup(grounds,'html.parser').text
    def get_keywords(self,number):
        sparql = SPARQLWrapper('https://publications.europa.eu/webapi/rdf/sparql')
        sparql.setReturnFormat(JSON)
        
        sparql.setQuery(f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?Keywords
        WHERE {{ 
            ?wc cdm:manifestation_case-law_keywords ?Keywords ;
                owl:sameAs ?w .
            FILTER (?w = <http://publications.europa.eu/resource/celex/{number}.ENG.txt>)
        }}
        LIMIT 100
        """)

        ret = sparql.queryAndConvert()

        keywords = ""
        for result in ret['results']['bindings']:
            keywords+=result['Keywords']['value']

        return BeautifulSoup(keywords,'html.parser').text

    def get_parties(self,number):
        sparql = SPARQLWrapper('https://publications.europa.eu/webapi/rdf/sparql')
        sparql.setReturnFormat(JSON)
        
        sparql.setQuery(f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?Parties
        WHERE {{ 
            ?wc cdm:manifestation_case-law_parties ?Parties ;
                owl:sameAs ?w .
            FILTER (?w = <http://publications.europa.eu/resource/celex/{number}.ENG.txt>)
        }}
        LIMIT 100
        """)

        ret = sparql.queryAndConvert()
        parties = ""
        for result in ret['results']['bindings']:
            parties+=result['Parties']['value']

        return BeautifulSoup(parties,'html.parser').text
    def get_subjects(self,number):
        sparql = SPARQLWrapper('https://publications.europa.eu/webapi/rdf/sparql')
        sparql.setReturnFormat(JSON)
        
        sparql.setQuery(f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?Subjects
        WHERE {{ 
            ?wc cdm:manifestation_case-law_subject ?Subjects ;
                owl:sameAs ?w .
            FILTER (?w = <http://publications.europa.eu/resource/celex/{number}.ENG.txt>)
        }}
        LIMIT 100
        """)

        ret = sparql.queryAndConvert()

        subjects = ""
        for result in ret['results']['bindings']:
            subjects+=result['Subjects']['value']

        return BeautifulSoup(subjects,'html.parser').text
    
    def get_citations(self,source_celex, cites_depth=1, cited_depth=1):
        """
        Gets all the citations one to X steps away. Hops can be specified as either
        the source document citing another (defined by `cites_depth`) or another document
        citing it (`cited_depth`). Any numbers higher than 1 denote that new source document
        citing a document of its own.
    
        This specific implementation does not care about intermediate steps, it simply finds
        anything X or fewer hops away without linking those together.
        """    
        sparql = SPARQLWrapper('https://publications.europa.eu/webapi/rdf/sparql')
        sparql.setReturnFormat(JSON)
        sparql.setQuery('''
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
            }''' % (source_celex, cites_depth, source_celex, cited_depth))
        ret = sparql.queryAndConvert()
    
        targets = set()
        for bind in ret['results']['bindings']:
            target = bind['name2']['value']
            targets.add(target)
        targets = list(set([el for el in list(targets)]))
            
        return targets
