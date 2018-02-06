def test_findDocument(self):
    wat = Watson()
    for docID in docIDToName:
        wat.findDocument(docID)

