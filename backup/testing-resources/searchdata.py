from operator import indexOf
import os
from generalHelperFunctions import changeLinkToFileName, changeFilenameToLink
from constants import  CONST_DROPTHRESHOLD
from  generalHelperFunctions import *
from  searchDataHelperFunctions import *   #This is in the end to prevent a circular import

# takes a url and returns the list of urls the url links to
def get_outgoing_links(linkString):
    filename = changeLinkToFileName(linkString)
    filepath = os.path.join('webData', filename)
    if os.path.isfile(filepath):
        with open('webData/' + filename, 'r') as file:
            data = file.readlines()
            if len(data) > 0:
                listLinks = (data[-1].strip())
                if 'http://' not in listLinks and 'https://' not in listLinks:
                    return None
            else:
                return None
            return listLinks.split(' ')
    return None


"""
It returns the pages where the respective url is present
:param url: The URL of the page you want to get the incoming links for
"""
def get_incoming_links(url):
    if not os.path.isdir('webData'):
        return None
    fileList = os.listdir('webData')
    urlList = []
    for recordFiles in fileList:
        with open('webData/'+recordFiles, 'r') as file:
            data = file.readlines()
            if len(data) > 0:
                listLinks = (data[-1])
                if (url) in listLinks:
                    urlList.append(changeFilenameToLink(recordFiles))
    if len(urlList) == 0:
        return None
    return urlList


"""
Returns the idf value for the word after reading it from the uniqueWordsIdf.txt file
:param word: the word whose idf we want to calculate
"""
def get_idf(word):
    with open('computationData/uniqueWordsIdf.txt', 'r') as idfFile:
        values = idfFile.readlines()
        for words in values:
            wordAndVal = words.strip().split('=')
            if wordAndVal[0] == word:
                return float(wordAndVal[1])
    return 0


"""
It returns the term frequency of a word in a given url that is stored in the urlComputations.txt file.

:param url: the url of the page
:param word: the word you want to search for
"""
def get_tf(url, word):
    with open('computationData/urlComputations.txt', 'r') as tfFile:
        data = tfFile.readlines()
        fileLength = len(data)
        loopCounter = 0
        while loopCounter <= fileLength-3:
            if data[loopCounter].strip() == url:
                requiredPageData = data[loopCounter +
                                        1].replace('=', ' ').strip().split(' ')
                try:
                    wordIndex = requiredPageData.index(word)+1
                except:
                    return 0
                wordIndex = requiredPageData.index(word)+1
                tf = float(requiredPageData[wordIndex])
                return tf
            loopCounter += 3
    return 0


# def get_tf_idf(url, word):
#     with open('computationData/urlComputations.txt', 'r') as tfFile:
#         data = tfFile.readlines()
#         fileLength = len(data)
#         loopCounter = 0
#         while loopCounter <= fileLength-3:
#             if data[loopCounter].strip() == url:
#                 requiredPageData = data[loopCounter +
#                                         2].replace('=', ' ').strip().split(' ')
#                 try:
#                     wordIndex = requiredPageData.index(word)+1
#                 except:
#                     return 0
#                 wordIndex = requiredPageData.index(word)+1
#                 tfidf = float(requiredPageData[wordIndex])
#                 return tfidf
#             loopCounter += 3
#     return 0

def get_tf_idf(url, word):
    with open('computationData/urlComputations.txt', 'r') as tfFile:
        data = tfFile.read().split('\n')
        try:
            urlIndex= data.index(url)
        except:
            return 0
        tfIdfIndex=urlIndex+2
        tdidfValues= data[tfIdfIndex].replace('=', ' ').strip().split(' ')
        try:
            wordIndex = tdidfValues.index(word)+1
        except:
            return 0
        tfidf = float(tdidfValues[wordIndex])
        return tfidf


# def get_page_rank(url):
#     urlIndexMap = generateUrlIndexMap()
#     probabilityTransitionMatrix = generate_probabilityTransitionMatrix(urlIndexMap)    #Instead of generating adj matrix first and only then the transition matrix, we directly calculate the transition matrix for efficiency.
#     scaledAdjacentMatrix = generate_scaled_adjacentMatrix(probabilityTransitionMatrix)
#     finalMatrix = generate_finalMatrix(scaledAdjacentMatrix)
#     piVector=[[1] + [0]* (len(urlIndexMap)-1)]   #First item is 1 and all other is 0. There's only 1 row and N columns.
#     euclidianDist=1
#     print('start')
#     while euclidianDist> CONST_DROPTHRESHOLD:
#         newVector=mult_matrix(piVector,finalMatrix)
#         prev=piVector
#         euclidianDist= euclidean_dist(prev, newVector)
#         piVector=newVector
#     for index, page in urlIndexMap.items():
#         if page==url: return piVector[0][index]
#     return -1


def get_page_rank(url):
    urlIndexMap = generateUrlIndexMap()
    urlOutgoings={}   #map all the urls to its outgoing links
    for pageUrl in urlIndexMap:
        urlOutgoings[pageUrl]= get_outgoing_links(pageUrl)
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
    try:
        return piVector[0][urlIndexMap[url]]
    except:
        return -1


# print(get_page_rank('http://people.scs.carleton.ca/~davidmckenney/fruits/N-770.html'))


