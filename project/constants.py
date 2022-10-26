""" 
These are the constant values that are used throughout the project.
"""




# To name the files as their urls. However, since some symbols are not supported in folder names, I want to replace the symbols with supporting ones (for windows| also works for apple).
symbolsMap = {
    '/': '^__^',
    ':': ';__;',
    '&#47': '@__@',  # for forward slash(\) symbol
    '|': '%__%',
    '*': '.__.',
    '?': '!__!',
    '>': '_]_',
    '<': '_[_',
    '"': "_'_"
}

CONST_ALPHA = 0.1                   #To calculate the transition probability and the transport matrices              
CONST_DROPTHRESHOLD= 0.0001             #Used to find out when the euclidian distance converges

allDirs=['webData', 'tf', 'idf', 'tfidf', 'pageRank']   #all the directories that are used to store data