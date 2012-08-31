
def getAllImgTagsAndLinks(url):
    """ Extract all the <img> tags, well just the really dumb ones without a 
        closing tag"""
    from re import finditer
    from urllib import urlopen
    try:
        pageContents = urlopen(url).read()
        allImgs = finditer("<img.*?>", pageContents)
        allHttpHrefs = finditer("href=\"(http.*?)\"", pageContents)
        
        allImgsTxt = "".join( (img.group(0) for img in allImgs))
        allHttpHrefs = "!-!".join( ( httpHref.group(1) for httpHref in allHttpHrefs) )
                              
        
        return ( allImgsTxt, allHttpHrefs) 
    except IOError:
        # page not found or something, ignore
        return ("", "")

        