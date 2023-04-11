import pandas as pd
def extract_containing_subject_matter(df,phrase):
    returner = df[df["LEGAL RESOURCE IS ABOUT SUBJECT MATTER"].str.contains(phrase, na=False)]
    return returner
def get_df_with_celexes(df,celexes):
    returner = df[df['CELEX IDENTIFIER'].isin(celexes)]
    return returner
def get_edges_list(df):
    extraction = df[['CELEX IDENTIFIER','citing']]
    extraction.reset_index(inplace=True)
    keys = extraction['CELEX IDENTIFIER']
    vals = extraction['citing']
    nodes = set()
    edges = list()
    for i in range(len(keys)):
        k = keys[i]
        val = vals[i]
        if val == val:
            nodes.add(str(k))
            val_unpacked = val.split(";")
            for val in val_unpacked:
                nodes.add(str(val))
                edges.append(str(k)+','+str(val))
        else:
            pass
    return edges, list(nodes)
def get_nodes_and_edges(df):
    edges, nodes = get_edges_list(df)
    #nodes = get_df_with_celexes(df,celexes)
    return nodes,edges