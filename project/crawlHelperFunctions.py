import os
import json
import math

from generalHelperFunctions import *
from constants import allDirs, CONST_DROPTHRESHOLD

# These are the extra functions that help the crawler.py crawl() function to carry out respective tasks.

""" 
Checks if a directory exists
:param dirname: string of the directory name
Returns True if dir exists
"""
def check_dir_exists(dirname):
    if os.path.isdir(dirname):
        return True
    else:
        return False



"""
This function clears the previous crawl's data from all the Directories.
"""
def clearPrevCrawl():
    for dir in allDirs:
        if not check_dir_exists(dir):
            os.mkdir(dir)
        else:
            dirFiles=os.listdir(dir)
            for file in dirFiles:
                os.remove(dir+'/'+file)

""" 
Adds the word, title and links data in json file for every url
:param url: url from which the data has been crawled
:param words, links: the string of words/ links contained in url seperated by a single space
:param title: string of the title of the url
"""
def addDataToFile(url, words, links, title):
    filename=changeLinkToFileName(url)+'.json'
    file = open('webData/'+filename, 'w')
    newData = {
        url: {
        'words': words,
        'links': links,
        'title': title
    }}
    json.dump(newData, file)
    file.close()

""" 
returns the idf value of a word
:param uniqueword: a string for the word for which the idf is generated
:param saveFile: a boolean flag which decides whether or not to save the idf values in a file or not.(It is used for the initialization of the idf values storing file)
"""
def generateIdf(uniqueWord, saveFile=False):
    wordCount = 0
    allFiles= get_url_list('webData')
    for file in allFiles:
        with open('webData/'+file, 'r') as dataFile:
            jsonData = json.load(dataFile)
            totalUrlNum = len(allFiles)
            for urls in jsonData:
                if uniqueWord in jsonData[urls]['words']:
                    wordCount += 1
    idf = math.log2(totalUrlNum/(1 + wordCount))
    if saveFile:
        if os.path.isfile('idf/words.json'):
            uniqueIdfsFile= open('idf/words.json', 'r+')

            uniqueWordsData = json.load(uniqueIdfsFile)
            newData = {uniqueWord: float(idf)}
            uniqueWordsData.update(newData)
            uniqueIdfsFile.seek(0)
        else:
            uniqueIdfsFile= open('idf/words.json', 'w')
            uniqueWordsData= {uniqueWord: float(idf)}
        json.dump(uniqueWordsData, uniqueIdfsFile)
        uniqueIdfsFile.close()
    return idf


"""
It generates the tf-idf matrix for the given pagesWordsCount and saves the data in a json file for every url.
:param pagesWordsCount: a dictionary that storest the frequencies of each unique word from each url of the form {page1: {word1: count1, word2: count2, ...}, page2:
{word1: count1, word2: count2, ...}, ...}
:param: uniqueWords: list of all the unique words from the crawled datas
"""
def generate_tf_tfIdf(pagesWordsCount, uniqueWords):
    # save tf and tf-idf values for all documents for all unique words in urlComputations.json file
    for url, wordsDict in pagesWordsCount.items():
        allTfs={}
        allTfIdfs={}
        finalTf = 0
        finalTfIdf = 0
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
            allTfs[uniqueItem] = (finalTf)
            allTfIdfs[uniqueItem] = (finalTfIdf)

        with open('tf/'+ changeLinkToFileName(url)+'.json', 'w') as computationFile:
            json.dump(allTfs, computationFile)

        with open('tfidf/'+ changeLinkToFileName(url)+'.json', 'w') as computationFile:
            json.dump(allTfIdfs, computationFile)

from searchDataHelperFunctions import *

def generate_pageRank(doc, allUrls, urlIndexMap, urlOutgoings):
    if (doc) not in allUrls: return -1
    probabilityTransitionMatrix = generate_probabilityTransitionMatrix(urlIndexMap, urlOutgoings)    #Instead of generating adj matrix first and only then the transition matrix, we directly calculate the transition matrix for efficiency.
    scaledAdjacentMatrix = generate_scaled_adjacentMatrix(probabilityTransitionMatrix)
    finalMatrix = generate_finalMatrix(scaledAdjacentMatrix)
    piVector=[[1] + [0]* (len(urlIndexMap)-1)]   #First item is 1 and all other is 0. There's only 1 row and N columns.
    euclidianDist=1
    while euclidianDist> CONST_DROPTHRESHOLD:
        newVector=mult_matrix(piVector,finalMatrix)
        prev=piVector
        euclidianDist= euclidean_dist(prev, newVector)
        piVector=newVector
    link=changeFilenameToLink(doc).replace('.json','')
    try:
        pageRank=  piVector[0][urlIndexMap[(link)]]
    except:
        return -1
    pageRank=  piVector[0][urlIndexMap[(link)]]
    pr_obj={'pageRank': pageRank}
    with open('pageRank/'+doc, 'w') as file:
        json.dump(pr_obj,file)


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