"""
This file contains some common MongoDB code.
"""
import os
import json
import pymongo as pm
from pymongo.server_api import ServerApi
import bson.json_util as bsutil


# all of these will eventually be put in the env:
user_nm = "jason"
cloud_svc = "scribble.hiydg.mongodb.net"
passwd = os.environ.get("MONGO_PASSWD", '')
cloud_mdb = "mongodb+srv"
db_params = "retryWrites=true&w=majority"

db_nm = 'scribbleDB'
if os.environ.get("TEST_MODE", ''):
    db_nm = "test_scribbleDB"

REMOTE = "0"
LOCAL = "1"

client = None


def get_client():
    """
    This provides a uniform way to get the client across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    """
    global client
    if os.environ.get("LOCAL_MONGO", REMOTE) == LOCAL:
        print("Connecting to Mongo locally.")
        client = pm.MongoClient()
    else:
        print("Connecting to Mongo remotely.")
        client = pm.MongoClient(f"mongodb+srv://jason:{passwd}@"
                                + f"{cloud_svc}/{db_nm}?"
                                + "retryWrites=true&w=majority",
                                server_api=ServerApi('1'))
    return client


def fetch_one(collect_nm, filters={}):
    """
    Fetch one record that meets filters for layers.
    """
    docs = []
    doc = client[db_nm][collect_nm].find_one(filters)
    docs.append(json.loads(bsutil.dumps(doc)))
    del docs[0]["_id"]
    del docs[0]["layer"]
    return docs


def fetch_one_raw(collect_nm, filters={}):
    """
    Fetch one record that meets filters.
    """
    docs = []
    doc = client[db_nm][collect_nm].find_one(filters)
    if doc is not None:
        docs.append(json.loads(bsutil.dumps(doc)))
        del docs[0]["_id"]
        return docs
    elif doc is None:
        return None


def del_one(collect_nm, filters={}):
    """
    Fetch one record that meets filters.
    """
    return client[db_nm][collect_nm].delete_one(filters)


def fetch_all(collect_nm):
    all_docs = []
    for doc in client[db_nm][collect_nm].find():
        docs = json.loads(bsutil.dumps(doc))
        del docs["_id"]
        del docs["layer"]
        all_docs.append(docs)

    return all_docs


def fetch_all_raw(collect_nm, key_nm):
    all_docs = []
    for doc in client[db_nm][collect_nm].find():
        docs = json.loads(bsutil.dumps(doc))
        all_docs.append(docs)

    return all_docs


def fetch_for_dropdown(collect_nm):
    lst = []
    raw = fetch_all(collect_nm)
    for doc in raw:
        temp = []
        for doc2 in list(doc.keys()):
            temp.append({"value": doc[doc2], "label": doc2})
        lst.append(temp)
    return lst


def fetch_all_as_dict(collect_nm, key_nm):
    all_list = fetch_all_raw(collect_nm, key_nm)
    print(f'{all_list=}')
    all_dict = {}
    for doc in all_list:
        print(f'{doc=}')
        all_dict[doc[key_nm]] = doc[key_nm]
    return all_dict


def fetch_all_as_list(collect_nm, key_nm):
    all_list = fetch_all_raw(collect_nm, key_nm)
    all_dict = {}
    for doc in all_list:
        all_dict[doc[key_nm]] = doc[key_nm]

    new_list = list(all_dict.keys())
    return new_list


def insert_doc(collect_nm, doc):
    client[db_nm][collect_nm].insert_one(doc)


def update_doc(collect_nm, doc, field):
    client[db_nm][collect_nm].update_one(doc, field)


def fetch_all_layers_as_dict(collect_nm, key_nm):
    all_list = fetch_all_raw(collect_nm, key_nm)
    all_dict = {}
    for doc in all_list:
        for field in doc:
            if(field != '_id' and field != 'layer'):
                all_dict[field] = doc[field]
    return all_dict
