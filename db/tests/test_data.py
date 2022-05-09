"""
This file holds the tests for db.py.
"""

from typing import Literal
from unittest import TestCase, skip
import random

import db.data as db

FAKE_USER = "Fake user"
LAYERS = ["body", "head", "eyes", "mouth"]

HUGE_NUM = 10000000000000  # any big number will do!


def new_entity_name(entity_type):
    int_name = random.randint(0, HUGE_NUM)
    return f"{entity_type}" + str(int_name)


class DBTestCase(TestCase):
    def test_get_layers(self):
        """
        Post-condition 1: return is a list.
        """
        ret = db.get_layers()
        return self.assertIsInstance(ret, list)

    def test_get_layers_for_dropdown(self):
        """
        Post-condition 1: return is a list.
        """
        ret = db.get_layers_for_dropdown()
        return self.assertIsInstance(ret, list)

    def test_get_layers_as_list(self):
        """
        Post-condition 1: return is a list.
        """
        ret = db.get_layers_as_list()
        return self.assertIsInstance(ret, list)

    def test_layer_exists(self):
        """
        Post-condition 1: return is a bool.
        """
        category = random.choice(LAYERS)
        name = new_entity_name("name")
        ret = db.layer_exists(category, name)
        return self.assertIsInstance(ret, bool)

    def test_add_layer(self):
        """
        Post-condition 1: return is a int.
        """
        category = random.choice(LAYERS)
        name = new_entity_name("name")
        link = new_entity_name("link")
        ret = db.add_layer(category, name, link)
        return self.assertIsInstance(ret, int)

    def test_user_exists(self):
        """
        Post-condition 1: return is a bool.
        """
        users = ["testing"]
        users.append(new_entity_name("user"))
        username = random.choice(users)
        ret = db.user_exists(username)
        return self.assertIsInstance(ret, bool)

    def test_add_user(self):
        """
        Post-condition 1: return is a int.
        """
        users = ["testing"]
        users.append(new_entity_name("user"))
        username = random.choice(users)
        password = new_entity_name("password")
        ret = db.add_user(username, password)
        return self.assertIsInstance(ret, int)

    def test_get_specific_user(self):
        """
        Post-condition 1: return is a list.
        """
        username = "testing"
        ret = db.get_specific_user(username)
        return self.assertIsInstance(ret, list)

    def test_check_credentials(self):
        """
        Post-condition 1: return is a bool.
        """
        users = ["testing"]
        users.append(new_entity_name("user"))
        username = random.choice(users)
        passw = ["testing"]
        passw.append(new_entity_name("password"))
        password = random.choice(passw)
        ret = db.check_credentials(username, password)
        return self.assertIsInstance(ret, bool)

    def test_add_scribble(self):
        """
        Post-condition 1: return is a int.
        """
        username = "testing"
        layers = db.get_layers()
        body = random.choice(list(layers[0].keys()))
        head = random.choice(list(layers[1].keys()))
        eyes = random.choice(list(layers[2].keys()))
        mouth = random.choice(list(layers[3].keys()))
        ret = db.add_scribble(username, body, head, eyes, mouth)
        return self.assertIsInstance(ret, int)

    def test_get_scribbles(self):
        """
        Post-condition 1: return is a list.
        """
        users = ["testing"]
        users.append(new_entity_name("user"))
        username = random.choice(users)
        ret = db.get_scribbles(username)
        return self.assertIsInstance(ret, list)