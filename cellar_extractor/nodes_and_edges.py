def extract_containing_subject_matter(df, phrase):
    returner = df[
        df["LEGAL RESOURCE IS ABOUT SUBJECT MATTER"].str.contains(phrase,
                                                                  na=False)
    ]
    return returner


def get_df_with_celexes(df, celexes):
    returner = df[df["CELEX IDENTIFIER"].isin(celexes)]
    return returner


def get_edges_list(df, only_local):
    extraction = df[["CELEX IDENTIFIER", "citing"]]
    extraction.reset_index(inplace=True)
    keys = extraction["CELEX IDENTIFIER"].tolist()
    vals = extraction["citing"].tolist()
    nodes = set()
    edges = list()
    for i in enumerate(keys):
        k = keys[i]
        val = vals[i]
        if val != val:
            continue
        nodes.add(str(k))
        val_unpacked = val.split(";")
        for val in val_unpacked:
            if only_local and val not in keys:
                continue
            nodes.add(str(val))
            edges.append(str(k) + "," + str(val))

    nodes = list(nodes)

    return edges, list(nodes)


def get_nodes_and_edges(df, only_local):
    edges, nodes = get_edges_list(df, only_local)
    # nodes = get_df_with_celexes(df,celexes)
    return nodes, edges
