"""
Get used to pymongo!
"""
import db_connect as dbc
import json
import bson.json_util as bsutil

client = dbc.get_client()

head_docs = []
doc = client[dbc.db_nm]['layers'].find_one({'layer': 'head'})

head_docs.append(json.loads(bsutil.dumps(doc)))
print(type(head_docs))
head_docs[0].pop("_id")


print(head_docs)
