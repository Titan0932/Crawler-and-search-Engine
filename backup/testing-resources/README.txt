""" for URL files in WebData 
    Each file stores all the data crawled from the corresponding URL

    filestructure is as follows: 
        
        # All lines before last line= uniquewords
        # last line= links
            -the links are seperated by spaces
        
"""
""" for files in computationData directory 

    filestructure is as follows: 
        1.) uniquewordsIdf.txt:
            It stores the idf value for each unique word present accross all the urls crawled
                -Each line is in the format=> Unique word: Idf value

        2.) urlComputations.txt
            It stores the tf and tf-Idf value for each Url.
                - For every sequential 3 lines:
                    - 1st line is the url
                    -second line is in the format => Uniqueword1= tfvalue1 Uniqueword2= tfvalue2 ......
                    -third line is in the format=> Uniqueword1= tfIdfvalue1 Uniqueword2= tfIdfvalue2 ......
"""
""" 
    for pageTitles.txt file: 
    It stores the titles of all respective urls:
        - Format => URL[SPACE]title

    filestructure is as follows: 
        
        # All lines before last line= uniquewords
        # last line= links
            -the links are seperated by spaces
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
        - These are all the fuunctions used by the searchData.py file in all its tasks.
    # searchHelperFunctions.py:
        - These are all the fuunctions used by the search.py file in all its tasks.
    # generalHelperFunctions.py:
        - These are all the functions used by multiple files.
    #constants.py:
        - It contains the constant variables whose values remain universal no matter where it is used. Also cannot be changed within program execution.
            - symbolsMap: map of all the symbols not supported by windows to the sybmols they are instead replaced by. (used while naming files as urls. Also works for apple devices)
            - ALPHA : the value used in the transition probability and the transport matrices calculations
            - CONST_DROPTHRESHOLD : value at which the euclidian distance converges.
    