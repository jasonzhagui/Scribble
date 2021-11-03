"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import os

DEMO_HOME = os.environ["DEMO_HOME"]

ROOMS_DB = f"{DEMO_HOME}/db/rooms.json"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2


def get_rooms():
    """
    A function to return all chat rooms.
    """
    try:
        with open(ROOMS_DB) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return None


def add_room(roomname):
    """
    add a room to the room database.
    """
    rooms = get_rooms()
    if rooms is None:
        return NOT_FOUND
    elif roomname in rooms:
        return DUPLICATE
    else:
        return OK
