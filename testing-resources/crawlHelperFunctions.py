import os
import json
import math

# These are the extra functions that help the crawler.py crawl() function to carry out respective tasks.

"""
This function clears the previous crawl's data from the webData Directory.
"""


def clearPrevCrawl():
    if os.path.isdir('webData'):
        fileList = os.listdir('webData')
        if len(fileList) > 0:
            for file in fileList:
                os.remove('webData/'+file)


""" 
Adds the word and links data in json file urlPageData.json for every url
:param url: url from which the data has been crawled
:param words, links: the string of words/ links contained in url seperated by a single space
:param title: string of the title of the url
"""
def addDataToFile(url, words, links, title):
    if not os.path.isdir('webData'):
        os.mkdir('webData')
    dirList = os.listdir('webData')
    if 'urlPageData.json' not in dirList:
        file = open('webData/urlPageData.json', 'w')
        jsonData = {
            url: {
                'words': words,
                'links': links,
                'title': title
            }}
    else:
        file = open('webData/urlPageData.json', 'r+')
        jsonData = json.load(file)
        newData = {url: {
            'words': words,
            'links': links,
            'title': title
        }}
        jsonData.update(newData)
        file.seek(0)
    json.dump(jsonData, file)
    file.close()

""" 
returns the idf value of a word
:param uniqueword: a string for the word for which the idf is generated
:param saveFile: a boolean flag which decides whether or not to save the idf values in a file or not.(It is used for the initialization of the idf values storing file)
"""

def generateIdf(uniqueWord, saveFile=False):
    dirList = os.listdir('webData')
    wordCount = 0
    with open('webData/urlPageData.json', 'r') as dataFile:
        jsonData = json.load(dataFile)
        totalUrlNum = len(jsonData)
        for urls in jsonData:
            if uniqueWord in jsonData[urls]['words']:
                wordCount += 1
    idf = math.log2(totalUrlNum/(1 + wordCount))
    if saveFile:
        if 'uniqueWordsIdf.json' not in dirList:
            uniqueIdfsFile= open('webData/uniqueWordsIdf.json', 'w')
            uniqueWordsData={
                uniqueWord: float(idf)
            }
        else:
            uniqueIdfsFile= open('webData/uniqueWordsIdf.json', 'r+')
            uniqueWordsData = json.load(uniqueIdfsFile)
            newData = {uniqueWord: float(idf)}
            uniqueWordsData.update(newData)
            uniqueIdfsFile.seek(0)
        json.dump(uniqueWordsData, uniqueIdfsFile)
    return idf


"""
It generates the tf-idf matrix for the given pagesWordsCount and saves the data in the webData/urlPageData.json file in json format.
:param pagesWordsCount: a dictionary that storest the frequencies of each unique word from each url of the form {page1: {word1: count1, word2: count2, ...}, page2:
{word1: count1, word2: count2, ...}, ...}
:param: uniqueWords: list of all the unique words from the crawled datas
"""
def generate_tf_tfIdf(pagesWordsCount, uniqueWords):
    # save tf and tf-idf values for all documents for all unique words in urlComputations.json file
    with open('webData/urlPageData.json', 'r+') as computationFile:
        jsonObject = json.load(computationFile)
        for url, wordsDict in pagesWordsCount.items():
            finalTf = ''
            finalTfIdf = ''
            newTf = 0
            for uniqueItem in uniqueWords:
                idf = generateIdf(uniqueItem)
                if uniqueItem not in pagesWordsCount[url]:
                    newTf = 0
                else:
                    newTf = wordsDict[uniqueItem] /pagesWordsCount[url]['totalWordNum']
                finalTf = float(newTf)
                newTfIdf = math.log2(1+newTf) * idf
                finalTfIdf = float(newTfIdf)
                if 'tf' in jsonObject[url]:    
                    jsonObject[url]['tf'][uniqueItem] = (finalTf)
                else:
                    jsonObject[url]['tf']={uniqueItem:finalTf}
                if 'tfidf' in jsonObject[url]:    
                    jsonObject[url]['tfidf'][uniqueItem] = (finalTfIdf)
                else:
                    jsonObject[url]['tfidf']={uniqueItem:finalTfIdf}

    with open('webData/urlPageData.json', 'w') as computationFile:
        json.dump(jsonObject, computationFile)


"""
It takes a string of an html page, parses it and returns the title, words , and links present in the page seperately.
:param linkString: The string that contains the Html page elements
:param activeUrl: The URL of the page that the user is currently on from which the string of links is obtained. This is necessary as if there is a relative url then the activeUrl can be used to form the whole url.
:param linkQueue: The list of unique urls which are sequentially to be crawled from.
"""
def getLinks(linkString, activeUrl, linkQueue):
    data = linkString.strip().split(' ')
    activeUrl = (activeUrl.split('/'))
    urls = ''
    for url in data:
        # removves the last index of the absolute url (i.e this page's address)
        activeUrl = activeUrl[0:-1]
        if 'http://' in url:  # check if its an absolute url or a relative url.
            finalUrl = url
        else:
            # only takes the link from the anchor tag
            url = url.replace('./', '')
            activeUrl.append(url)  # and adds the current link's url
            finalUrl = '/'.join(activeUrl)
        urls += finalUrl + ' '
        if finalUrl not in linkQueue:  # check if the url is already in the queue
            linkQueue.append(finalUrl)
    return urls


"""
It parses the html file and extracts the links and words from it.

:param string: the html string
:param linkQueue: A queue of links to be parsed
:param url: the url of the page from where we're parsing
:param pagesWordsCount: a dictionary that keeps track of the number of words in each page
:param uniqueWords: a dictionary that contains all the unique words in the pages that have been
parsed so far
"""
def parseHtml(string, linkQueue, url, pagesWordsCount, uniqueWords):
    activeLoop = True
    words = ''
    links = ''
    titleFound = False
    while activeLoop:
        # for <title>
        if not titleFound:
            titleStartIndex = string.find('<title>')
            endIndex = string.find('</title>')
            title = string[titleStartIndex+7:endIndex]
            string = string.replace(string[titleStartIndex:endIndex+7], '')
            titleFound = True
        # for <p>
        pStartIndex = string.find('<p>')
        if pStartIndex != -1:
            endIndex = string.find('</p>')
            words += ' '+string[pStartIndex+3:endIndex].replace('\n', ' ')
            string = string.replace(string[pStartIndex:endIndex+3], '')

        # for <a> tag
        aStartIndex = string.find('<a ')
        if aStartIndex != -1:
            endIndex = aStartIndex + string[aStartIndex:].find('>')
            # reference position of href attribute from the postion of the <a tag, taken from 0.
            hrefIndex = string[aStartIndex:endIndex].find('href="')
            links += ' ' + string[aStartIndex+hrefIndex+6:endIndex-1]
            closingTag = string.find('</a>')
            string = string.replace(string[aStartIndex:closingTag+3], '')

        # for <p....> tag with attributes
        pAttributeStartIndex = string.find('<p ')
        if pAttributeStartIndex != -1:
            end_IndexOf_StartingTag = string[pAttributeStartIndex:].find('>')
            closingTag = string.find('</p>')
            words += ' '+string[end_IndexOf_StartingTag+1:closingTag]
        if titleFound and pStartIndex == -1 and aStartIndex == -1 and pAttributeStartIndex == -1:
            activeLoop = False

    fulllinks = getLinks(links, url, linkQueue)
    for word in words.strip().split(' '):
        if word != '':
            pagesWordsCount[url]['totalWordNum'] += 1
            if word not in uniqueWords:
                uniqueWords.append(word)
            if word in pagesWordsCount[url]:
                pagesWordsCount[url][word] += 1
            else:
                pagesWordsCount[url][word] = 1
    return title, words, fulllinks


""" 
Deletes the first item of a queue of list datatype
:param queue: a list of items which abstractly works as a queue
"""
def dequeue(queue):
    return queue[1:]