"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import os

import db.db_connect as dbc

SCRIBBLE_HOME = os.environ["SCRIBBLE_HOME"]

ROOMS = "rooms"
USERS = "users"

# field names in our DB:
USER_NM = "userName"
ROOM_NM = "roomName"
NUM_USERS = "num_users"

LAYERS = "layers"

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
    return dbc.fetch_all(ROOMS, ROOM_NM)


def get_layers():
    """
    A function to return a list of all layers.
    """
    return dbc.fetch_all(LAYERS, LAYER)


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


def get_rooms_as_dict():
    """
    A function to return a dictionary of all rooms.
    """
    return dbc.fetch_all_as_dict(ROOMS, ROOM_NM)


def room_exists(roomname):
    """
    See if a room with roomname is in the db.
    Returns True of False.
    """
    rec = dbc.fetch_one(ROOMS, filters={ROOM_NM: roomname})
    print(f"{rec=}")
    return rec is not None


def layer_exists(category, name):
    """
    See if a layer with name is in the db.
    Returns True or False.
    """
    rec = dbc.fetch_one(LAYERS, filters={LAYER: category})
    rec = rec[0].get(name)
    print(f"{rec=}")
    return rec is not None


def del_room(roomname):
    """
    Delete roomname from the db.
    """
    if not room_exists(roomname):
        return NOT_FOUND
    else:
        dbc.del_one(ROOMS, filters={ROOM_NM: roomname})
        return OK


def add_room(roomname):
    """
    Add a room to the room database.
    """
    print(f"{roomname=}")
    if room_exists(roomname):
        return DUPLICATE
    else:
        dbc.insert_doc(ROOMS, {ROOM_NM: roomname, NUM_USERS: 0})
        return OK


def add_layer(category, name, link):
    """
    Add a layer to the layer database.
    """
    print(f"{name=}")
    if layer_exists(category, name):
        return DUPLICATE
    else:
        dbc.insert_doc(LAYERS, {LAYER: category, name: link})
        return OK


def user_exists(username):
    """
    See if a user with username is in the db.
    Returns True of False.
    """
    rec = dbc.fetch_one(USERS, filters={USER_NM: username})
    print(f"{rec=}")
    return rec is not None


def get_users():
    """
    A function to return a list of all users.
    """
    return dbc.fetch_all(USERS, USER_NM)


def add_user(username):
    """
    Add a user to the user database.
    Until we are using a real DB, we have a potential
    race condition here.
    """
    if user_exists(username):
        return DUPLICATE
    else:
        dbc.insert_doc(USERS, {USER_NM: username})
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
