import os
from searchdata import get_idf, get_page_rank
import math

#These are the extra functions required by the search() function in the search.py file


"""
    returns the list of urls crawled that is present in the webData directory
"""
def get_url_list():
    if os.path.isdir('webData'):
        fileList = os.listdir('webData')
    return fileList

"""
It takes a phrase as input and returns the tf-idf score of the words in the phrase in the form of a dictionary.
:param phrase: string of words seperated by spaces
"""
def get_query_tfIdf(phrase):
    queryVector={}    # map of words and their tfIdf values in the query
    uniqueWords=[]    #list of unique words in the query
    phraseList=phrase.strip().split(' ')    #list of words in the query
    totalWords= len(phraseList)
    wordCount={}          #dictionary which counts the frequency of words in the query entered
    for word in phraseList:
        if word not in uniqueWords:
            uniqueWords.append(word)
            wordCount[word]=0    #initializing values
    for word in phraseList:
        wordCount[word] +=1
    for uniqueWord in uniqueWords:
        tf= wordCount[uniqueWord]/totalWords
        idf= get_idf(uniqueWord)
        queryVector[uniqueWord]=(math.log2(1+ tf) * idf)
    return queryVector


"""
It calculates the score by multiplying the score of each url by its pagerank value and returns the updated score dict.
:param cosine_similarity: dictionary of the cosine similarity of every url.
"""
def calcScoreByboost(cosine_similarity):
    score={}
    for url in cosine_similarity:
        score[url]= cosine_similarity[url] * get_page_rank(url)
        # print('calculated')
    # print('donee')
    return score


"""
It returns list of the url titles of all the urls that was crawled and stored in pageTitles.txt file.
"""
def get_url_titles():
    titles={}
    with open('pageTitles.txt','r') as file:
        urlTitles=file.readlines()
        for urlTitle in urlTitles:
            urlTitle=urlTitle.split(' ')
            url=urlTitle[0]
            title=urlTitle[1]
            titles[url]=title
    return titles