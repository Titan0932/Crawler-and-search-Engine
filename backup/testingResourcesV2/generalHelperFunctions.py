
from constants import symbolsMap
"""
It changes the link to the file name by replacing unsupported symbols as in the symbolsMap variable.
:param link: link to be renamed
"""
def changeLinkToFileName(link):
    for key, value in symbolsMap.items():
        link = link.replace(key, value)
    return link

"""
It takes the link that had some unsupported symbols so that it could be used as a folder name and returns the actual link by replacing the replaced symbols
:param name: The name of the file to be changed to a link
"""
def changeFilenameToLink(name):
    for key, value in symbolsMap.items():
        name = name.replace(value, key)
    return name
