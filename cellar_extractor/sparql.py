from SPARQLWrapper import SPARQLWrapper, JSON, CSV, POST
import requests


def run_eurlex_webservice_query(query_input, username, password):
    target = "https://eur-lex.europa.eu/EURLexWebService?wsdl"
    query = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sear="http://eur-lex.europa.eu/search">
      <soap:Header>
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" soap:mustUnderstand="true">
          <wsse:UsernameToken xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="UsernameToken-1">
            <wsse:Username>%s</wsse:Username>
            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">%s</wsse:Password>
          </wsse:UsernameToken>
        </wsse:Security>
      </soap:Header>
      <soap:Body>
        <sear:searchRequest>
          <sear:expertQuery><![CDATA[%s]]></sear:expertQuery>
          <sear:page>1</sear:page>
          <sear:pageSize>100</sear:pageSize>
          <sear:searchLanguage>en</sear:searchLanguage>
        </sear:searchRequest>
      </soap:Body>
    </soap:Envelope>""" % (
        username,
        password,
        query_input,
    )
    return requests.request("POST", target, data=query, allow_redirects=True)


def get_citations(source_celex, cites_depth=1, cited_depth=1):
    """
    Method acquired from a different law and tech project
    for getting the citations of a
    source_celex.
    Unlike get_citations_csv, only works for one source celex at once.
    Returns a set containing all the works cited by the source celex.
    Gets all the citations one to X steps away. Hops can be specified as either
    the source document citing another (defined by `cites_depth`)
    or another document
    citing it (`cited_depth`). Any numbers higher than 1 denote that
    new source document
    citing a document of its own.

    This specific implementation does not care about intermediate steps,
    it simply finds
    anything X or fewer hops away without linking those together.
    """
    sparql = SPARQLWrapper("https://publications.europa.eu/webapi/rdf/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(
        """
        prefix cdm: <https://publications.europa.eu/ontology/cdm#>
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
    try:
        ret = sparql.queryAndConvert()
    except Exception:
        return get_citations(source_celex)
    targets = set()
    for bind in ret["results"]["bindings"]:
        target = bind["name2"]["value"]
        targets.add(target)
    # Filters the list. Filter type: '3'=legislation, '6'=case law.
    targets = set([el for el in list(targets)])
    return targets


def get_citations_csv(celex):
    """
    Method sending a query to the endpoint,
    which asks for cited works for each celex.
    The celex variable in the method is a list of
    all the celex identifiers of the
    cases we need the citations of.
    The query returns a csv, containing all of the data needed."""
    endpoint = "https://publications.europa.eu/webapi/rdf/sparql"
    input_celex = '", "'.join(celex)
    query = """
           prefix cdm: <https://publications.europa.eu/ontology/cdm#>
 prefix xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT DISTINCT * WHERE
        {
        {
            SELECT ?celex ?citedD WHERE {
                ?doc cdm:resource_legal_id_celex ?celex
                 FILTER(STR(?celex) in ("%s")).
                ?doc cdm:work_cites_work{1,1} ?cited .
                ?cited cdm:resource_legal_id_celex ?citedD .
            }
        } UNION {
            SELECT ?celex ?citedD WHERE {
                ?doc cdm:resource_legal_id_celex ?celex
                 FILTER(STR(?celex) in ("%s")).
                ?cited cdm:work_cites_work{1,1} ?doc .
                ?cited cdm:resource_legal_id_celex ?citedD .
            }
        }
}
       """ % (
        input_celex,
        input_celex,
    )

    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(CSV)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    try:
        ret = sparql.queryAndConvert()
    except Exception:
        return get_citations_csv(celex)
    return ret.decode("utf-8")


def get_citing(celex, cites_depth):
    endpoint = "https://publications.europa.eu/webapi/rdf/sparql"
    input_celex = '", "'.join(celex)
    query = """
           prefix cdm: <https://publications.europa.eu/ontology/cdm#>
 prefix xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT DISTINCT * WHERE
        {
            SELECT ?celex ?citedD WHERE {
                ?doc cdm:resource_legal_id_celex ?celex
                 FILTER(STR(?celex) in ("%s")).
                ?doc cdm:work_cites_work{1,%i} ?cited .
                ?cited cdm:resource_legal_id_celex ?citedD .
            }
}
       """ % (
        input_celex,
        cites_depth,
    )

    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(CSV)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    try:
        ret = sparql.queryAndConvert()
    except Exception:
        return get_citing(celex, cites_depth)
    return ret.decode("utf-8")


def get_cited(celex, cited_depth):
    endpoint = "https://publications.europa.eu/webapi/rdf/sparql"
    input_celex = '", "'.join(celex)
    query = """
           prefix cdm: <https://publications.europa.eu/ontology/cdm#>
 prefix xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT DISTINCT * WHERE
        {
            SELECT ?celex ?citedD WHERE {
                ?doc cdm:resource_legal_id_celex ?celex
                 FILTER(STR(?celex) in ("%s")).
                ?cited cdm:work_cites_work{1,%i} ?doc .
                ?cited cdm:resource_legal_id_celex ?citedD .
            }
}
       """ % (
        input_celex,
        cited_depth,
    )

    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(CSV)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    try:
        ret = sparql.queryAndConvert()
    except Exception:
        return get_cited(celex, cited_depth)
    return ret.decode("utf-8")
