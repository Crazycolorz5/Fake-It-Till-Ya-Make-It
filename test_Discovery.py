from Discovery import *

def test_findDocument():
    wat = Watson()
    for docID in docIDToName:
        wat.findDocument(docID)

