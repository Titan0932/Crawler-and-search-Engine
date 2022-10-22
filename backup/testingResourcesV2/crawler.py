import os
import webdev
from  generalHelperFunctions import *
from  crawlHelperFunctions import *


# maps all the data found from a url using the url as its key in the dictionary
crawledData = {}
# A list that stores the links that are to be crawled/ or is already crawled. The queue keeps on getting filled as new links come in and the links are simultaneously accessed as the loop happens.
# The accessed items arent removed as we only need to access them once and their precence in the list means that it has been/or will be accessed once only.
linkQueue = []
uniqueWords = []  #list of all the unique words that are present in all of the urls crawled

## CHECK THE README.TXT file for file information

def crawl(seed):
    clearPrevCrawl()
    linkQueue.append(seed)
    pagesWordsCount = {  # {pageURL : {'totalWordNum': totalWordsInURL,'uniqueWord1': count1, uniqueWord2: count2,.........,}}   #this dictionary stores the tfs for every page. This dict is used such that we can compute the values as the crawl loop is active simultaneously such that another loop does not have to be used to compute these values.
    }
    for url in (linkQueue):
        data = webdev.read_url(url)
        pagesWordsCount[url] = {'totalWordNum': 0}
        title, words, links= parseHtml(data, linkQueue, url, pagesWordsCount,uniqueWords)
        add_titles_to_file(url, title)
        createDataFile(changeLinkToFileName(url), words+'\n'+ links)
    if not os.path.isdir('computationData'):   #all computed data is stored in the computationData directory
        os.mkdir('computationData')
    for uniqueItem in uniqueWords:      #generate and save the idf value for all unique words in a file
        generateIdf(uniqueItem, saveFile=True)

    generate_tf_tfIdf(pagesWordsCount, uniqueWords)
    return len(linkQueue)

# crawl('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html')