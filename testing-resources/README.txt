""" for files in WebData 
    
    1.) urlPageData.json:
        It stores all the crawled data and computed values for search for every interlinked url in json format.
        The format is: 
            {
                url:{
                    words: [...],
                    links:[...],
                    title: ..,
                    tf: {word: tf,..},
                    tfidf:{word:tfidf...}
                }
            }
    2.) uniqueWordsIdf.json:
        It stores all the unique words from the crawled urls and stores the idf correspondingly.
        The format is:
            {
                word1: idf1,
                word2: idf2,
                ...
            }
"""

#Navigating through the project:
    # crawler.py:
        -crawler function in  crawls the data and creates all the aforementioned files.
    # searchdata.py: 
        - The functions in searchdata.py are used to retrieve certain data after crawling is done 
    # search.py:
        - The search() function is used to generate the result list which contains a sorted list of the top 10 urls and their titles and their search score based on the search score in descending order 

    # crawlHelperFunctions.py:
        - These are all the functions used by the crawler.py file in its tasks.
    #searchDataHelperFunctions.py:
        - These are all the functions used by the searchData.py file in all its tasks.
    # searchHelperFunctions.py:
        - These are all the functions used by the search.py file in all its tasks.
    #constants.py:
        - It contains the constant variables whose values remain universal no matter where it is used. Also cannot be changed within program execution.
            - ALPHA : the value used in the transition probability and the transport matrices calculations
            - CONST_DROPTHRESHOLD : value at which the euclidian distance converges.
    