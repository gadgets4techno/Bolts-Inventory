from cloudant import Cloudant
import os, json
from pathlib import Path

g=Path("inventory","vcap-local.json")
with open(g) as f:
    vcap = json.load(f)
    print('Found local VCAP_SERVICES')
    creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
    user = creds['username']
    password = creds['password']
    url = 'https://' + creds['host']
    client = Cloudant(user, password, url=url, connect=True)
    # db = client.create_database(db_name, throw_on_exists=False)

client.connect()
db = client["bolts-parts"]
def getpart():
    pass
selector={"_id":{"$gt":{}}}
result = db.get_query_result(selector, fields=["part","description","quantity"])

for doc in result:
    print(doc)


client.disconnect()