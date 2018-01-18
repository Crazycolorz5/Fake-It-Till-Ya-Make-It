import json
from watson_developer_cloud import DiscoveryV1

discovery = DiscoveryV1(
  username="{username}",
  password="{password}",
  version="2017-11-07"
)

response = discovery.create_environment(
  name="my_environment",
  description="My environment",
  size=1
)


new_collection = discovery.create_collection(response["environment_id"], 'my_collection', description='The main collection for all documents.', configuration_id='{configuration_id}', language='{language}')

print(response) #json.dumps(response, indent=2))
