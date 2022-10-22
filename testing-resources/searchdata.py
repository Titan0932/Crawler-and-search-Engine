import os
from constants import  CONST_DROPTHRESHOLD
from  searchDataHelperFunctions import *
import json

# takes a url and returns the list of urls the url links to
def get_outgoing_links(linkString):
    with open('webData/urlPageData.json', 'r') as file:
        data = json.load(file)
        if linkString not in data: return None
        urlData=data[linkString]['links'].strip()
        if len(urlData) == 0 or ('http://' not in urlData and 'https://' not in urlData):
            return None
        return urlData.split(' ')


"""
It returns the pages where the respective url is present
:param url: The URL of the page you want to get the incoming links for
"""
def get_incoming_links(url):
    if not os.path.isdir('webData'):
        return None
    urlList = []
    with open('webData/urlPageData.json','r') as file:
        fileData= json.load(file)
        for pageUrl in fileData:
            if len(fileData[pageUrl]['links']) > 0:
                if (url) in fileData[pageUrl]['links']:
                    urlList.append(pageUrl)
    if len(urlList) == 0:
        return None
    return urlList


"""
Returns the idf value for the word after reading it from the uniqueWordsIdf.json file
:param word: the word whose idf we want to calculate
"""
def get_idf(word):
    with open('webData/uniqueWordsIdf.json', 'r') as idfFile:
        jsonData = json.load(idfFile)
        if word in jsonData.keys():
            return jsonData[word]
    return 0


"""
It returns the term frequency of a word in a given url that is stored in the urlComputations.json file.

:param url: the url of the page
:param word: the word you want to search for
"""
def get_tf(url, word):
    with open('webData/urlPageData.json', 'r') as tfFile:
        json_object=json.load(tfFile)
        if url in json_object:
            urlData= json_object[url]['tf']
            if word in urlData:
                tf= urlData[word]
                return float(tf)
    return 0


def get_tf_idf(url, word):
    with open('webData/urlPageData.json', 'r') as tfFile:
        json_object=json.load(tfFile)
        if url in json_object:
            urlData= json_object[url]['tfidf']
            if word in urlData:
                tfidf= urlData[word]
                return float(tfidf)
    return 0


def get_page_rank(url):
    allUrls= get_url_list()
    if url not in allUrls: return -1
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


from searchHelperFunctions import get_url_list
