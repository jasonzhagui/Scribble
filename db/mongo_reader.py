"""
Get used to pymongo!
"""
import db_connect as dbc

COLLECT_NAME = 'layers'


client = dbc.get_client()
print(f"{client=}")

this_collect = client[dbc.db_nm][COLLECT_NAME]


doc = client[dbc.db_nm][COLLECT_NAME].find_one({'layer': 'head'})
# print(f"find one = {doc=}")
print(doc["lemon"])
