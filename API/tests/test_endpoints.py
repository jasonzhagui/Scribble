"""
This file holds the tests for endpoints.py.
"""

from unittest import TestCase, skip 
from flask_restx import Resource, Api
import random

import API.endpoints as ep
import db.data as db
import db.db_connect as dbc

HUGE_NUM = 10000000000000  # any big number will do!


def new_entity_name(entity_type):
    int_name = random.randint(0, HUGE_NUM)
    return f"{entity_type}" + str(int_name)


class EndpointTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hello(self):
        hello = ep.HelloWorld(Resource)
        ret = hello.get()
        self.assertIsInstance(ret, dict)
        self.assertIn(ep.HELLO, ret)

    def test_list_layers(self):
        """
        Post-condition 1: return is a list.
        """
        ll = ep.ListLayers(Resource)
        ret = ll.get()
        self.assertIsInstance(ret, list)

    def test_create_layers(self):
        """
        See if we can successfully create a new layer.
        Post-condition: room is in DB.
        """
        cl = ep.CreateLayer(Resource)
        new_category = random.choice(db.get_layers_as_list())
        new_name = new_entity_name("name")
        new_link = new_entity_name("link")
        ret = cl.post(new_category, new_name, new_link)
        print(f'post {ret=}')
        layers = db.get_layers()
        print(f'{layers=}')
        self.assertIn(new_name, {k:v for x in layers for k,v in x.items()})

    def test_dropdown_list_layers(self):
        """
        Post-condition 1: return is a list.
        """
        dll = ep.DropdownListLayers(Resource)
        ret = dll.get()
        self.assertIsInstance(ret, list)

    def test_check_credentials(self):
        """
        See if we can successfully check inputted credentials.
        Post-condition: bool.
        """
        cc = ep.CheckCredentials(Resource)

        username = ["test"]
        password = ["password"]
        username.append(new_entity_name("user"))
        password.append(new_entity_name("pass"))

        user = random.choice(username)	
        passw = random.choice(password)

        print("Username: ", user)
        print("Password: ", passw)
        ret = cc.get(user, passw)
        print("Credentials: " + str(ret))
        self.assertIsInstance(ret, bool)

    def test_register(self):
        """
        See if we can successfully register user.
        Post-condition: user is in db.
        """
        reg = ep.Register(Resource)
        new_user = new_entity_name("user")
        new_password = (new_entity_name("pass"))
        ret = reg.post(new_user, new_password)
        print(f'post {ret=}')
        users = db.get_specific_user(new_user)
        print(f'{users=}')
        self.assertEqual(new_user, users[0]['username'])

    def test_create_scribble(self):
        """
        See if we can successfully add a scribble.
        Post-condition: scribble is in db.
        """
        cs = ep.CreateScribble(Resource)
        lst = db.get_layers()
        username = new_entity_name("user")
        body = random.choice(list(lst[0]))
        head = random.choice(list(lst[1]))
        eyes = random.choice(list(lst[2]))
        mouth = random.choice(list(lst[3]))
        doc = {
                "body": lst[0][body],
                "head": lst[1][head],
                "eyes": lst[2][eyes],
                "mouth": lst[3][mouth]}
        ret = cs.post(username, body, head, eyes ,mouth)
        print(f'post {ret=}')
        print(f'added {doc=}')
        scribbles = db.get_scribbles(username)
        print(f'{scribbles=}')
        self.assertIn(doc, scribbles)

    def test_get_scribbles(self):
        """
        Post-condition 1: return is a list.
        """
        gs = ep.GetScribbles(Resource)
        ret = gs.get("jason")
        self.assertIsInstance(ret, list)
