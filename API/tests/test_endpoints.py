"""
This file holds the tests for endpoints.py.
"""

from unittest import TestCase, skip 
from flask_restx import Resource, Api
import random

import API.endpoints as ep
import db.data as db

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

    def test_list_head_layers(self):
        """
        Post-condition 1: return is a list.
        """
        ll = ep.ListAllHeads(Resource)
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
        layers = db.get_all_layers_as_dict()
        print(f'{layers=}')
        self.assertIn(new_name, layers)

