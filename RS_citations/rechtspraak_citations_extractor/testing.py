import pandas as pd


from citations_extractor import get_citations

if __name__ == '__main__':
    data = pd.read_csv('echr_metadata_0-ALL_dates_2023-01-01-END.csv')
    df_in, df_out, df_leg = get_citations(data,'','',1)
    df_in.to_csv('caselaw_incoming.csv', index=False)
    df_out.to_csv('caselaw_outgoing.csv', index=False)
    df_leg.to_csv('legislations_cited.csv', index=False)