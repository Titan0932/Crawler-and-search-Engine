import os

from generalHelperFunctions import *
import json

# takes a url and returns the list of urls the url links to
def get_outgoing_links(linkString):
    filename=changeLinkToFileName(linkString)+'.json'
    if not os.path.isfile('webData/'+filename): return None
    with open('webData/'+filename, 'r') as file:
        data = json.load(file)
        urlData=data[linkString]['links'].strip()
        if len(urlData) == 0 or ('http://' not in urlData and 'https://' not in urlData):
            return None
        return urlData.split(' ')


"""
It returns the pages where the respective url is present
:param url: The URL of the page you want to get the incoming links for
"""
def get_incoming_links(url):
    allUrls=os.listdir('webData')
    urlList = []
    for pageData in allUrls:
        with open('webData/'+pageData,'r') as file:
            fileData= json.load(file)
            link=changeFilenameToLink(pageData).replace('.json','')
            if len(fileData[link]['links']) > 0:
                if (url) in fileData[link]['links']:
                    urlList.append(link)
    if len(urlList) == 0:
        return None
    return urlList

"""
Returns the idf value for the word after reading it from the uniqueWordsIdf.json file
:param word: the word whose idf we want to calculate
"""
def get_idf(word):
    with open('idf/words.json', 'r') as idfFile:
        jsonData = json.load(idfFile)
        if word in list(jsonData.keys()):
            return jsonData[word]
    return 0


"""
It returns the term frequency of a word in a given url that is stored in the urlComputations.json file.

:param url: the url of the page
:param word: the word you want to search for
"""
def get_tf(url, word):
    filename=changeLinkToFileName(url)+'.json'
    if not os.path.isfile('tf/'+filename): return 0
    with open('tf/'+ filename, 'r') as tfFile:
        json_object=json.load(tfFile)
        if word in json_object:
            tf= json_object[word]
            return float(tf)
    return 0

def get_tf_idf(url, word):
    filename=changeLinkToFileName(url)+'.json'
    if not os.path.isfile('tfidf/'+filename): return 0
    with open('tfidf/'+ filename, 'r') as tfFile:
        json_object=json.load(tfFile)
        if word in json_object:
            tfidf= json_object[word]
            return float(tfidf)
    return 0

def get_page_rank(url):
    filename=changeLinkToFileName(url)+'.json'
    if not os.path.isfile('pageRank/'+filename): return -1
    with open('pageRank/'+filename,'r') as file:
        data=json.load(file)
        return float(data['pageRank'])
