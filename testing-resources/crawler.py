import webdev
from  crawlHelperFunctions import *


# A list that stores the links that are to be crawled/ or is already crawled. The queue keeps on getting filled as new links come in and the links are simultaneously accessed as the loop happens.
linkQueue = []
import time
## CHECK THE README.TXT file for file information
def crawl(seed):
    start=time.time()
    uniqueWords = []  #list of all the unique words that are present in all of the urls crawled
    linksAccessed=0   #the counter for the number of links accessed
    clearPrevCrawl()
    linkQueue.append(seed)
    pagesWordsCount = {  # {pageURL : {'totalWordNum': totalWordsInURL,'uniqueWord1': count1, uniqueWord2: count2,.........,}}   #this dictionary stores the tfs for every page. This dict is used such that we can compute the values as the crawl loop is active simultaneously such that another loop does not have to be used to compute these values.
    }
    for url in (linkQueue):
        data = webdev.read_url(url)
        pagesWordsCount[url] = {'totalWordNum': 0}
        title, words, links= parseHtml(data, linkQueue, url, pagesWordsCount,uniqueWords)
        addDataToFile(url, words,links,title)
        dequeue(linkQueue)
        linksAccessed+=1
    for uniqueItem in uniqueWords:      #generate and save the idf value for all unique words in a file
        generateIdf(uniqueItem, saveFile=True)

    generate_tf_tfIdf(pagesWordsCount, uniqueWords)
    end=time.time()
    print(end-start)
    return linksAccessed

crawl('http://people.scs.carleton.ca/~davidmckenney/fruits/N-0.html')