import math
from searchdata import get_tf_idf, changeFilenameToLink
from  searchHelperFunctions import *

""" 
:param phrase: string of multiple words seperated by spaces
:param boost: boolean value that determines if the page's content score should be boosted by the page's pagerank score.
"""
def search(phrase, boost):
    queryVectorDict= get_query_tfIdf(phrase)
    urlList= get_url_list()    #list of all urls
    cosine_similarity={}    
    for url in urlList:
        url= changeFilenameToLink(url)
        numerator=0
        leftDenominator=0
        rightDenominator=0
        for wordInQuery in queryVectorDict:
            doc_tfIdf= get_tf_idf(url,wordInQuery)
            query_tfIdf= queryVectorDict[wordInQuery]
            numerator+= query_tfIdf * doc_tfIdf
            leftDenominator+= query_tfIdf ** 2
            rightDenominator+= doc_tfIdf ** 2
            # print(numerator, leftDenominator, rightDenominator)
        denominator=  (math.sqrt(leftDenominator) * math.sqrt(rightDenominator))
        if denominator==0:
            cosineSim=0
        else:
            cosineSim= (numerator)/ denominator
        cosine_similarity[url] = cosineSim
    # print('startingggg')
    if boost:
        scores = calcScoreByboost(cosine_similarity)
    else:
        scores= cosine_similarity
    # print(scores)
    scores= dict((sorted(scores.items(), key=lambda x: x[1], reverse=True) )[0:10])
    titles=get_url_titles()
    result= []
    for url in scores:
        result.append({'url': url, 'title': titles[url].strip(), 'score': scores[url]})
    # print(scores)
    # print(result)
    return result

# search('peach banana pear pear peach coconut peach banana',True)
