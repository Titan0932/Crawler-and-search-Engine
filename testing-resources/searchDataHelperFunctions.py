from constants import *
import json

#These are the extra functions that help the searchData.py functions.


"""
for all the url files crawled and stored in webData/urlPageData.json, it creates an index map for all the urls
return a dictionary of {url: index} 
"""
def generateUrlIndexMap():
    urlIndexMap = {}
    with open('webData/urlPageData.json', 'r') as file:
        json_object= json.load(file)
        for index,url in enumerate(json_object):
            urlIndexMap[url]= index 
    return urlIndexMap

"""
It generates a link transition matrix from the given urlIndexMap.
:param urlIndexMap: A dictionary that maps a URL to an index.
:param urlOutgoings: A dictionary that maps a url to its outgoing links
"""
def generate_probabilityTransitionMatrix(urlIndexMap, urlOutgoings):
    totalPages = len(urlIndexMap)
    adjacencyMatrix = []
    for pageUrl in urlIndexMap:
        urlOutgoingLinks = urlOutgoings[pageUrl]
        totalOnes = len(urlOutgoingLinks)
        newMatrix = []
        availableones = totalOnes  # counter for ho wmany outgoing links are left
        if totalOnes == 0:  # if no put going links then all elements=1/N
            newMatrix = [0] * totalPages
        else:
            for pageIndex, page in enumerate(urlIndexMap):
                if availableones == 0:  # To make it a bit efficient as if no more 1s is left we know all that follows is 0 and we can terminate loop
                    newMatrix += [0] * (totalPages - pageIndex)
                    break
                if page in urlOutgoingLinks:
                    newMatrix.append(1/totalOnes)
                    availableones -= 1
                else:
                    newMatrix.append(0)
        adjacencyMatrix.append(newMatrix)
    return adjacencyMatrix

"""
It generates a new matrix after scalar multiplication with the generated adj matrix with a factor of (1-Alpha) 
:param probabilityTransitionMatrix: 2-D matrix which already has all the probabilitities mapped for all links
"""
def generate_scaled_adjacentMatrix(probabilityTransitionMatrix):   #PS I used the same code in Tutorial 4 for scalar multiplication
    newMatrix = probabilityTransitionMatrix[:]
    for rowIndex, row in enumerate(probabilityTransitionMatrix):
        for itemIndex, item in enumerate(row):
            newMatrix[rowIndex][itemIndex] = item*(1-CONST_ALPHA)
    return newMatrix

"""
It generates the final matrix after considering the random transport value and adds it to the result of (1-Alpha)*probabilitytransitionMatrix 
:param scaledAdjacentMatrix: result matrix of (1-Alpha)*probabilitytransitionMatrix 
"""
def generate_finalMatrix(scaledAdjacentMatrix):   #PS I used the same code in Tutorial 4 for scalar multiplication
    newMatrix = scaledAdjacentMatrix[:]
    matrixLength= len(scaledAdjacentMatrix)
    for rowIndex, row in enumerate(scaledAdjacentMatrix):
        for itemIndex in range(len(row)):
            newMatrix[rowIndex][itemIndex]+=(CONST_ALPHA/matrixLength)
    return newMatrix

"""
It multiplies two matrices together.
:param a,b: matrices to be multiplied
"""
def mult_matrix(matrixX, matrixY):                       #PS I used the same code in Tutorial 4 for matrix multiplication
    resultMatrix=[]
    for rowx in range(len(matrixX)):
        resultMatrix.append([])
        for coly in range(len(matrixY[0])):
            colValue=0
            for rowy in range(len(matrixY)):
                colValue+=matrixX[rowx][rowy] * matrixY[rowy][coly]
            resultMatrix[rowx].append(colValue)
    # print('donedanadandan')
    return resultMatrix

""" 
Finds the euclidian distance between two matrices
:param a,b: matrices of whose the euclidian distance is to be calculated
"""
def euclidean_dist(a,b):     #PS I used the same code in Tutorial 4
	eDistance=0
	if len(a)>1 or len(b)>1:
		return -1
	for itemA,itemB in zip(a[0],b[0]):
		eDistance+= (itemA-itemB) ** 2
	return (eDistance ) **0.5

