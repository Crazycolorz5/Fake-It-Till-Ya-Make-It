import json
from watson_developer_cloud import DiscoveryV1

discovery = DiscoveryV1(
  username="9b933574-a27e-407c-961e-f8ab10d8ad5d",
  password="IpRnfb244XuP",
  version="2017-11-07"
)
environment_id = "14f0004b-c966-4644-89b7-b5465bcbc116"
collection_id = "f13d7ea8-a3bb-4f87-bd0f-bba7cb3b94d3"


collection = discovery.get_collection(environment_id, collection_id)
print(json.dumps(collection, indent=2))

qopts = {'query': "Wikipedia", "passages" : True}
my_query = discovery.query(environment_id, collection_id, qopts)
print(json.dumps(my_query, indent=2))
