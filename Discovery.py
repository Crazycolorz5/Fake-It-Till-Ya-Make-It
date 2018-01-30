import json
from watson_developer_cloud import DiscoveryV1
from sys import argv

discovery = DiscoveryV1(
  username="9b933574-a27e-407c-961e-f8ab10d8ad5d",
  password="IpRnfb244XuP",
  version="2017-11-07"
)
environment_id = "14f0004b-c966-4644-89b7-b5465bcbc116"
collection_id = "f13d7ea8-a3bb-4f87-bd0f-bba7cb3b94d3"

def askWatson(query, found_documents):
    qopts = {'natural_language_query': query, 'passages' : True, 'passages.count' : 3, 'count' : 0}
    my_query = discovery.query(environment_id, collection_id, qopts)
    results = my_query["passages"]
    return list(filter(lambda x: x['document_id'] in found_documents, results))


found_documents = set()
print("Results for your query:")
print(askWatson(argv[1], found_documents))

print()
print("You found a document on mitosis!")
found_documents.add('ad9d680ed1a99a7c856a89991d25d6f7')

print("Results for your query:")
print(askWatson(argv[1], found_documents))


