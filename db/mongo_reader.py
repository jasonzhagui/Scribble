"""
Get used to pymongo!
"""
import db_connect as dbc
import json
import bson.json_util as bsutil

COLLECT_NAME = 'layers'


client = dbc.get_client()
print(f"{client=}")

this_collect = client[dbc.db_nm][COLLECT_NAME]

head_docs = []
doc = client[dbc.db_nm][COLLECT_NAME].find_one({'layer': 'head'})
# print(f"find one = {doc=}")

head_docs.append(json.loads(bsutil.dumps(doc)))
print(head_docs)
