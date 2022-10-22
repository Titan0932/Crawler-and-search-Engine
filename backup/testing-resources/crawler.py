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
        linksList = ''
        data = webdev.read_url(url)
        pagesWordsCount[url] = {'totalWordNum': 0}
        title, words, links= parseHtml(data, linkQueue, url, pagesWordsCount,uniqueWords)
        # print(url)
        # print(links)
        # print(title)
        # print(words)
        # print('\n')
        # such that we can create seperate arrays for texts within the <p> tag and for other tags.
        # data = data.replace('</p>', '<p>')
        # data = data.split('<p>')                # same as above
        # data[0] = data[0].replace('</title>', '<title>')
        # title = data[0].split('<title>')[1]
        # data[0] = data[0].replace('<html>', '',).replace('<body>', '').replace('<title>', '').replace(
        #     title, '').replace('<head>', '').replace('</head>', '')  # remove head and html tags
        add_titles_to_file(url, title)
        # # now that we have seperated the <p> tags we need to extract the words within them. So we split them based on '\n' creating another array of words.
        # dataToAdd=''
        # for item in (data):
        #     if '<a href="' in item:
        #         # store all the links present in the page in strings
        #         linksList += getLinks(item, url, linkQueue)
        #     else:
        #         dataToAdd += item.lstrip()
        # for word in dataToAdd.strip().split('\n'):
        #     if word != '':
        #         pagesWordsCount[url]['totalWordNum'] += 1
        #         if word not in uniqueWords:
        #             uniqueWords.append(word)
        #         if word in pagesWordsCount[url]:
        #             pagesWordsCount[url][word] += 1
        #         else:
        #             pagesWordsCount[url][word] = 1
        # # to ensure that all the links present is added in the last line of the file
        # dataToAdd += linksList
        createDataFile(changeLinkToFileName(url), words+'\n'+ links)
    for uniqueItem in uniqueWords:      #generate and save the idf value for all unique words in a file
        generateIdf(uniqueItem, saveFile=True)

    generate_tf_tfIdf(pagesWordsCount, uniqueWords)
    return len(linkQueue)

crawl('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html')