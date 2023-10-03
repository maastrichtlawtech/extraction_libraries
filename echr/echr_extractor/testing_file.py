import logging
import sys
from os.path import abspath

import echr_extractor

current_dir = (abspath(__file__))
correct_dir = '\\'.join(current_dir.replace('\\', '/').split('/')[:-2])
sys.path.append(correct_dir)
# print(sys.path)


if __name__ == '__main__':
    link = 'https://hudoc.echr.coe.int/eng#%7B%22fulltext%22:[%22(NOT%20%5C%22has%20been%20a%20violation%20of%20Article%206%5C%22)%20AND%20(%5C%22has%20been%20no%20violation%20of%20Article%206%5C%22)%22]%7D'
    logging.info('hey')

    """
    
    
    %20AND%20((NOT%20%22has%20been%20a%20violation%20of%20Article%206%22)%20AND%20(%22has%20been%20no%20violation%20of%20Article%206%22))
    VS
    
    %20AND%20((NOT%20%22has%20been%20a%20violation%20of%20Article%206%22)%20AND%20(%22has%20been%20no%20violation%20of%20Article%206%22))
    
    
    
    
    https://hudoc.echr.coe.int/app/query/results?query=contentsitename%3AECHR%20AND%20(NOT%20(doctype%3DPR%20OR%20doctype%3DHFCOMOLD%20OR%20doctype%3DHECOMOLD))    %20AND%20((NOT%20%22has%20been%20a%20violation%20of%20Article%206%22)%20AND%20(%22has%20been%20no%20violation%20of%20Article%206%22))&select=itemid,applicability,appno,article,conclusion,docname,doctype,doctypebranch,ecli,importance,judgementdate,languageisocode,originatingbody,violation,nonviolation,extractedappno,scl,publishedby,representedby,respondent,separateopinion,sharepointid,externalsources,issue,referencedate,rulesofcourt,DocId,WorkId,Rank,Author,Size,Path,Description,Write,CollapsingStatus,HighlightedSummary,HighlightedProperties,contentclass,PictureThumbnailURL,ServerRedirectedURL,ServerRedirectedEmbedURL,ServerRedirectedPreviewURL,FileExtension,ContentTypeId,ParentLink,ViewsLifeTime,ViewsRecent,SectionNames,SectionIndexes,SiteLogo,SiteDescription,deeplinks,SiteName,IsDocument,LastModifiedTime,FileType,IsContainer,WebTemplate,SecondaryFileExtension,docaclmeta,OriginalPath,EditorOWSUSER,DisplayAuthor,ResultTypeIdList,PartitionId,UrlZone,AAMEnabledManagedProperties,ResultTypeId,rendertemplateid&sort=itemid%20Ascending&start=0&length=1
    """
    df = echr_extractor.get_echr(link=link)
    b = 2
