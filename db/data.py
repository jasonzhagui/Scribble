"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import os

import db.db_connect as dbc

SCRIBBLE_HOME = os.environ["SCRIBBLE_HOME"]

ROOMS = "rooms"

# field names in our DB:
USER_NM = "username"
PASSWORD = "password"

ROOM_NM = "roomName"
NUM_USERS = "num_users"

USERS = "users"
LAYERS = "layers"
SCRIBBLES = "scribbles"

LAYER = "layer"
HEAD = "head"


OK = 0
NOT_FOUND = 1
DUPLICATE = 2


client = dbc.get_client()
if client is None:
    print("Failed to connect to MongoDB.")
    exit(1)


def get_rooms():
    """
    A function to return a list of all rooms.
    """
    return dbc.fetch_all_raw(ROOMS, ROOM_NM)


def get_layers():
    """
    A function to return a list of all layers.
    """
    return dbc.fetch_all(LAYERS)


def get_layers_for_dropdown():
    return dbc.fetch_for_dropdown(LAYERS)


def get_layers_as_dict():
    """
    A function to return a dictionary of all layers.
    """
    return dbc.fetch_all_as_dict(LAYERS, LAYER)


def get_all_layers_as_dict():
    """
    A function to return a dictionary of all items.
    """
    return dbc.fetch_all_layers_as_dict(LAYERS, LAYER)


def get_layers_as_list():
    """
    A function to return a dictionary of all layers.
    """
    return dbc.fetch_all_as_list(LAYERS, LAYER)


def get_head_layers():
    """
    A function to return a list of all head layers.
    """
    return dbc.fetch_one(LAYERS, filters={LAYER: HEAD})


def get_specific_layer(category):
    """
     A function to return a list of layers by category input.
    """
    return dbc.fetch_one(LAYERS, filters={LAYER: category})


def layer_exists(category, name):
    """
    See if a layer with name is in the db.
    Returns True or False.
    """
    rec = dbc.fetch_one(LAYERS, filters={LAYER: category})
    rec = rec[0].get(name)
    print(f"{rec=}")
    return rec is not None


def add_layer(category, name, link):
    """
    Add a layer to the layer database.
    """
    print(f"{name=}")
    if layer_exists(category, name):
        return DUPLICATE
    else:
        dbc.update_doc(LAYERS, {LAYER: category}, {"$set": {name: link}})
        return OK


def user_exists(username):
    """
    See if a user with username is in the db.
    Returns True of False.
    """
    rec = dbc.fetch_one_raw(USERS, filters={USER_NM: username})
    print(f"{rec=}")
    return rec is not None


def get_users():
    """
    A function to return a list of all users.
    """
    return dbc.fetch_all_raw(USERS, USER_NM)


def add_user(username, password):
    """
    Add a user to the user database.
    Until we are using a real DB, we have a potential
    race condition here.
    """
    if user_exists(username):
        return DUPLICATE
    else:
        dbc.insert_doc(USERS, {USER_NM: username, PASSWORD: password})
        return OK


def del_user(username):
    """
    Delete username from the db.
    """
    if not user_exists(username):
        return NOT_FOUND
    else:
        dbc.del_one(USERS, filters={USER_NM: username})
        return OK


def get_specific_user(username):
    """
    See if a user with username is in the db.
    Returns username and password if exists.
    """
    return dbc.fetch_one_raw(USERS, filters={USER_NM: username})


def check_credentials(username, password):
    """
    Check the username and password input against what's in the database
    """
    doc = dbc.fetch_one_raw(USERS, filters={USER_NM: username})
    if doc is None:
        return False
    elif password != doc[0].get(PASSWORD):
        return False
    elif password == doc[0].get(PASSWORD):
        return True


def add_scribble(username, body, head, eyes, mouth):
    lst = get_layers()
    doc = {
            "username": username,
            "body": lst[0][body],
            "head": lst[1][head],
            "eyes": lst[2][eyes],
            "mouth": lst[3][mouth]}

    all_list = dbc.fetch_all_raw(SCRIBBLES, username)

    for i in range(len(all_list)):
        item = all_list[i]
        del item["_id"]
        if doc == item:
            return DUPLICATE

    dbc.insert_doc(SCRIBBLES, doc)
    return OK


def get_scribbles(username):
    doc = dbc.fetch_all_raw(SCRIBBLES, username)
    for item in doc:
        del item["_id"]
        del item["username"]
    return doc
