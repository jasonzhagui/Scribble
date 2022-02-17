"""
Get used to pymongo!
"""
import db_connect as dbc
import json
import bson.json_util as bsutil

client = dbc.get_client()

head_docs = []
doc = client[dbc.db_nm]['layers'].find_one({'layer': 'head'})

head_docs = (json.loads(bsutil.dumps(doc)))
print(head_docs['lemon'])
del head_docs['_id']
print(head_docs)