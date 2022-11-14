from SPARQLWrapper import SPARQLWrapper, JSON, POST


def get_all_eclis(starting_date=None, ending_date=None):
    """Gets a list of all ECLIs in CELLAR. If this needs to be picked up from a previous run,
    the last ECLI parsed in that run can be used as starting point for this run

    :param starting_date: Document modification date to start off from.
        Can be set to last run to only get updated documents.
        Ex. 2020-03-19T09:41:10.351+01:00
    :type starting_date: str, optional
    :param ending_date: Document modification date to end at.
    :type ending_date : str,optional
    :return:  A list of all (filtered) ECLIs in CELLAR.
    :rtype: list[str]
    """

    # This query essentially gets all things from cellar that have an ECLI.
    # It then sorts that list, and if necessary filters it based on an ECLI to start off from.
    endpoint = 'https://publications.europa.eu/webapi/rdf/sparql'
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)

    sparql.setQuery('''
        prefix cdm: <http://publications.europa.eu/ontology/cdm#> 
        select 
        distinct ?ecli
        where { 
            ?doc cdm:case-law_ecli ?ecli .
            ?doc <http://publications.europa.eu/ontology/cdm/cmr#lastModificationDate> ?date .
            %s
            %s
        }
        order by asc(?ecli)
    ''' % (
        f'FILTER(STR(?date) >= "{starting_date}")' if starting_date else '',
        f'FILTER(STR(?date) <= "{ending_date}")' if ending_date else ''
    )
                    )
    ret = sparql.queryAndConvert()

    eclis = []

    # Extract the actual results
    for res in ret['results']['bindings']:
        eclis.append(res['ecli']['value'])

    return eclis


def get_raw_cellar_metadata(eclis, get_labels=True, force_readable_cols=True, force_readable_vals=False):
    """Gets cellar metadata

    :param eclis: The ECLIs for which to retrieve metadata
    :type eclis: list[str]
    :param get_labels: Flag to get human-readable labels for the properties, defaults to True
    :type get_labels: bool, optional
    :param force_readable_cols: Flag to remove any non-labelled properties from the resulting dict, defaults to True
    :type force_readable_cols: bool, optional
    :param force_readable_vals: Flag to remove any non-labelled values from the resulting dict, defaults to False
    :type force_readable_vals: bool, optional
    :return: Dictionary containing metadata. Top-level keys are ECLIs, second level are property names
    :rtype: Dict[str, Dict[str, list[str]]]
    """

    # Find every outgoing edge from an ECLI document and return it (essentially giving s -p> o)
    # Also get labels for p/o (optionally) and then make sure to only return distinct triples
    endpoint = 'https://publications.europa.eu/webapi/rdf/sparql'
    query = '''
        prefix cdm: <http://publications.europa.eu/ontology/cdm#> 
        prefix skos: <http://www.w3.org/2004/02/skos/core#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select 
        distinct ?ecli ?p ?o ?plabel ?olabel
        where { 
            ?doc cdm:case-law_ecli ?ecli .
            FILTER(STR(?ecli) in ("%s"))
            ?doc ?p ?o .
            OPTIONAL {
                ?p rdfs:label ?plabel
            }
            OPTIONAL {
                ?o skos:prefLabel ?olabel .
                FILTER(lang(?olabel) = "en") .
            }
        }
    ''' % ('", "'.join(eclis))

    sparql = SPARQLWrapper(endpoint)

    sparql.setReturnFormat(JSON)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    try:
        ret = sparql.queryAndConvert()
    except Exception:
        return get_raw_cellar_metadata(eclis, get_labels, force_readable_cols, force_readable_vals)
    # Create one dict for each document
    metadata = {}
    for ecli in eclis:
        metadata[ecli] = {}

    # Take each triple, check which source doc it belongs to, key/value pair into its dict derived from the p and o in
    # the query
    for res in ret['results']['bindings']:
        ecli = res['ecli']['value']
        # We only want cdm predicates
        if not res['p']['value'].startswith('http://publications.europa.eu/ontology/cdm'):
            continue

        # Check if we have predicate labels
        if 'plabel' in res and get_labels:
            key = res['plabel']['value']
        elif force_readable_cols:
            continue
        else:
            key = res['p']['value']
            key = key.split('#')[1]

        # Check if we have target labels
        if 'olabel' in res and get_labels:
            val = res['olabel']['value']
        elif force_readable_vals:
            continue
        else:
            val = res['o']['value']

        # We store the values for each property in a list. For some properties this is not necessary,
        # but if a property can be assigned multiple times, this is important. Notable, for example is citations.b
        if key in metadata[ecli]:
            metadata[ecli][key].append(val)
        else:
            metadata[ecli][key] = [val]

    return metadata
