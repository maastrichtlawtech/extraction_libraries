from echr import get_echr_extra, get_echr
import dateutil.parser



if __name__ == '__main__':
    #df,json = get_echr_extra(count=100,save_file='y',threads=10)

    """
    Start and end dates must be date objects, which can be achieved by calling dateutil.parser.parse(some date string).date().
    I assume you dont want to do that in this file but im not sure where this conversion is most appropriate so I'll leave it up to you.
    Note that there is an extra import because of this.
    I have commented out some of your stuff to test this, if you run it as is it should work. @Benjamin
    """

    fields = ['itemid', 'applicability', 'application', 'appno', 'article', 'conclusion', 'decisiondate',
              'docname', 'documentcollectionid', 'documentcollectionid2', 'doctype', 'doctypebranch',
              'ecli', 'externalsources', 'extractedappno', 'importance', 'introductiondate',
              'isplaceholder', 'issue', 'judgementdate', 'kpdate', 'kpdateAsText', 'kpthesaurus',
              'languageisocode', 'meetingnumber', 'originatingbody', 'publishedby', 'Rank',
              'referencedate', 'reportdate', 'representedby','resolutiondate', 'resolutionnumber', 
              'respondent', 'respondentOrderEng', 'rulesofcourt', 'separateopinion', 'scl',
              'sharepointid', 'typedescription', 'nonviolation', 'violation']
    df = get_echr(start_date="22-03-2010", end_date="22-01-2020")
    #b=2
    #df,json = get_echr_extra(start_id=20,end_id=3000,save_file='n')

    #df = get_echr(start_id=1000,count=2000,save_file='n')

