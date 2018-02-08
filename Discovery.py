# Example Usage:
# >>> from Discovery import *
# >>> a = Watson()
# >>> a.ask("What treaty ended the War of 1812?")
# []
# >>> a.findDocument(docNameToID['War of 1812 - Wikipedia'])
# >>> a.ask("What treaty ended the War of 1812?")
# ['in subsequent decades.\n\nLong-term consequences\n\nMain article: Results of the War of 1812\n\nNeither side lost territory in the war, nor did the treaty that ended it address the original points of contention—and yet it changed much between the United States of America and Britain.', 'The resulting Siege of Fort Mackinac on July 17 was the first major land engagement of the war, and ended in an easy British victory.\n\nCourse of war\n\nSee also: Timeline of the War of 1812\n\nThe war was conducted', 'News of the treaty arrived shortly thereafter, halting military operations. The treaty was unanimously ratified by the United States on February 17, 1815, ending the war with <a href="/wiki/Status_quo_ante_bellum" title="Status quo ante bellum">Status quo ante bellum</a> (no boundary changes).']
# >>> 

import json
from watson_developer_cloud import DiscoveryV1
from itertools import islice

discovery = DiscoveryV1(
  username="9b933574-a27e-407c-961e-f8ab10d8ad5d",
  password="IpRnfb244XuP",
  version="2017-11-07"
)
environment_id = "14f0004b-c966-4644-89b7-b5465bcbc116"
collection_id = "f13d7ea8-a3bb-4f87-bd0f-bba7cb3b94d3"

docIDToName = dict()
docNameToID = dict()

docIDToName['181f74c2c11aede44654b969e5d18676'] = "A Tale of Two Cities - Wikipedia"
docIDToName['ad9d680ed1a99a7c856a89991d25d6f7'] = "Mitosis - Wikipedia"
docIDToName['27ce78f83dc0d72d96e3f5766736992d'] = "Quadratic Equation - Wikipedia"
docIDToName['98e9b50f1327e045364f669dab17a2ea'] = "War of 1812 - Wikipedia"

docNameToID = { docIDToName[iden] : iden for iden in docIDToName } #Invert the previous dictionary.

class Watson:
    NUM_RESULTS = 3
    
    def __init__(self):
        self.foundDocuments = set()
        self.cachedQueries = dict()
        
    def ask(self, query):
        if query in self.cachedQueries:
            return self.processResults(self.cachedQueries[query])
        qopts = {'natural_language_query': query, 'passages' : True, 'count' : 0} #'passages.count' : 3
        myQuery = discovery.query(environment_id, collection_id, qopts)
        results = myQuery["passages"]
        self.cachedQueries[query] = results
        return self.processResults(results)

    def findDocument(self, identifier):
        self.foundDocuments.add(identifier)

    def processResults(self, passages):
        return list(map(lambda x: x['passage_text'], 
                islice(
                filter(lambda x: x['document_id'] in self.foundDocuments, 
                    passages),
                Watson.NUM_RESULTS)))
    

# found_documents = set()
# print("Results for your query:")
# print(askWatson(argv[1], found_documents))

# print()
# print("You found a document on mitosis!")
# found_documents.add('ad9d680ed1a99a7c856a89991d25d6f7')

# print("Results for your query:")
# print(askWatson(argv[1], found_documents))


