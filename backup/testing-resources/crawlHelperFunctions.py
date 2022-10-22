import os
import math

#These are the extra functions that help the crawler.py crawl() function to carry out respective tasks.

"""
This function clears the previous crawl's data from the webData Directory, pagesTitles.txt and computationData directory (if any).
"""
def clearPrevCrawl():
    if os.path.isdir('webData'):
        fileList = os.listdir('webData')
        if len(fileList) > 0:
            for file in fileList:
                os.remove('webData/'+file)

    if os.path.isdir('computationData'):
        fileList = os.listdir('computationData')
        if len(fileList) > 0:
            for file in fileList:
                os.remove('computationData/'+file)
    
""" 
Creates a file for every url and populatesit with the data crawled
:param filename: name of the file (the url which has been modified according to the symbolsMap Constant)
:param data: the data that was crawled from the corresponding url
"""
def createDataFile(filename, data):
    if not os.path.isdir('webData'):
        os.mkdir('webData')
    with open('webData/'+filename, 'w') as newFile:
        newFile.write(data)



""" 
returns the idf value of a word
:param uniqueword: a string for the word for which the idf is generated
:param safeFile: a boolean flag which decides whether or not to save the idf values in a file or not.(It is used for the initialization of the idf values storing file)
"""
def generateIdf(uniqueWord, saveFile=False):
    totalDocsList = os.listdir('webData')
    totalDocsNum = len(totalDocsList)
    wordCount = 0
    with open('computationData/uniqueWordsIdf.txt', 'a') as uniqueIdfsFile:
        for doc in totalDocsList:
            with open('webData/' + doc, 'r') as datafile:
                data = datafile.read().split('\n')
                if uniqueWord in data:
                    wordCount += 1
        idf = math.log2(totalDocsNum/(1 + wordCount))
        if saveFile:
            uniqueIdfsFile.write(uniqueWord+'='+str(idf)+'\n')
    return idf


"""
It generates the tf-idf matrix for the given pagesWordsCount and saves the data in the computationData/urlComputations.txt file.
:param pagesWordsCount: a dictionary that storest the frequencies of each unique word from each url of the form {page1: {word1: count1, word2: count2, ...}, page2:
{word1: count1, word2: count2, ...}, ...}
:param: uniqueWords: list of all the unique words from the crawled datas
"""
def generate_tf_tfIdf(pagesWordsCount, uniqueWords):
    with open('computationData/urlComputations.txt', 'a') as computationFile:    # save tf and tf-idf values for all documents for all unique words in urlComputations.txt file
        for url, wordsDict in pagesWordsCount.items():
            finalTf = ''
            finalTfIdf = ''
            newTf = 0
            for uniqueItem in uniqueWords:
                idf = generateIdf(uniqueItem)
                if uniqueItem not in pagesWordsCount[url]:
                    newTf = 0
                else:
                    newTf = wordsDict[uniqueItem] / pagesWordsCount[url]['totalWordNum']
                finalTf += f'{uniqueItem}={newTf} '
                newTrIdf = math.log2(1+newTf) * idf
                finalTfIdf += f'{uniqueItem}={newTrIdf} '
            computationFile.write(url+'\n'+str(finalTf) +
                                  '\n' + str(finalTfIdf)+'\n')

"""
Creates a new file where in each line there is: pageurl[SPACE]title 
:param url: string of the page url
:param title: string of the tile of the corresponding title
"""
def add_titles_to_file(url,title):
    with open('pageTitles.txt','a') as file:
        file.write(url+' '+title+'\n')

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

def parseHtml(string,linkQueue, url, pagesWordsCount,uniqueWords):
    activeLoop=True
    words=''
    links=''
    titleFound=False
    while activeLoop:
        #for <title>
        if not titleFound:
            titleStartIndex=string.find('<title>')
            endIndex=string.find('</title>')
            title=string[titleStartIndex+7:endIndex]
            string=string.replace(string[titleStartIndex:endIndex+7],'')
            titleFound=True
        #for <p>
        pStartIndex=string.find('<p>')
        if pStartIndex!=-1:
            endIndex=string.find('</p>')
            words+=' '+string[pStartIndex+3:endIndex]
            string=string.replace(string[pStartIndex:endIndex+3],'')
            
        #for <a> tag
        aStartIndex=string.find('<a ')
        if aStartIndex!=-1:
            endIndex=aStartIndex+ string[aStartIndex:].find('>')
            hrefIndex=string[aStartIndex:endIndex].find('href="')     #reference position of href attribute from the postion of the <a tag, taken from 0.
            links+=' '+ string[aStartIndex+hrefIndex+6:endIndex-1]
            closingTag=string.find('</a>')
            string=string.replace(string[aStartIndex:closingTag+3],'')

        #for <p....> tag with attributes
        pAttributeStartIndex=string.find('<p ')
        if pAttributeStartIndex!=-1:
            end_IndexOf_StartingTag=string[pAttributeStartIndex:].find('>')
            closingTag=string.find('</p>')
            words+=' '+string[end_IndexOf_StartingTag+1:closingTag]
        if titleFound and pStartIndex==-1 and aStartIndex==-1 and pAttributeStartIndex==-1:
            activeLoop=False

    fulllinks= getLinks(links,url, linkQueue)
    for word in words.strip().split(' '):
        if word != '':
            pagesWordsCount[url]['totalWordNum'] += 1
            if word not in uniqueWords:
                uniqueWords.append(word)
            if word in pagesWordsCount[url]:
                pagesWordsCount[url][word] += 1
            else:
                pagesWordsCount[url][word] = 1
    return title,words, fulllinks
        


""" PREVIOUS VERSIONS OF FUnCTIONS:: JUST HERE FOR REFERENCE AND BACKUP """

"""
It takes a string of links and an active URL, and adds the urls found in the string to the linkQueue dictionary for all urls not already in the dictionary. It also returns the string of urls
:param linkString: The string that contains the <a href></a> tags for each link.
:param activeUrl: The URL of the page that the user is currently on from which the string of links is obtained. This is necessary as if there is a relative url then the activeUrl can be used to form the whole url.
"""
# def getLinks(linkString, activeUrl, linkQueue):
#     data = linkString.replace(
#         '</body>', '').replace('</html>', '').strip().split('\n')

#     activeUrl = (activeUrl.split('/'))
#     urls = ''
#     for url in data:
#         # removves the last index of the absolute url (i.e this page's address)
#         activeUrl = activeUrl[0:-1]
#         if 'http://' in url:  # check if its an absolute url or a relative url.
#             finalUrl = url
#         else:
#             # only takes the link from the anchor tag
#             url = url.split('"')[1].replace('./', '')
#             activeUrl.append(url)  # and adds the current link's url
#             finalUrl = '/'.join(activeUrl)
#         urls += finalUrl + ' '
#         if finalUrl not in linkQueue:  # check if the url is already in the queue
#             linkQueue.append(finalUrl)
#     return urls
