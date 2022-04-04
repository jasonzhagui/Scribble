"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus
from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
import werkzeug.exceptions as wz

import db.data as db

app = Flask(__name__)
CORS(app)
api = Api(app)

HELLO = 'Hola'
WORLD = 'mundo'


@api.route('/hello')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO: WORLD}


@api.route('/layers/list')
class ListLayers(Resource):
    """
    This endpoint returns a list of all layers.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns a list of all layers.
        """
        layers = db.get_layers()
        if layers is None:
            raise (wz.NotFound("layers db not found."))
        else:
            return layers


@api.route('/layers/heads')
class ListAllHeads(Resource):
    """
    This endpoint returns a list of all head layers.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns a list of all head layers.
        """
        head_layers = db.get_head_layers()
        if head_layers is None:
            raise (wz.NotFound("head layers db not found."))
        else:
            return head_layers


@api.route('/layers/<category>')
class ListSpecificLayer(Resource):
    """
    This endpoint returns a list of layers by category input.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, category):
        """
        Returns a list of layers by category input.
        """
        layer = db.get_specific_layer(category)
        if layer is None:
            raise (wz.NotFound("layers db not found."))
        else:
            return layer


@api.route('/layers/dropdownList')
class DropdownListLayers(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        layers = db.get_layers_for_dropdown()
        if layers is None:
            raise (wz.NotFound("layers db not found."))
        else:
            return layers


@api.route('/layers/<category>/<name>')
class GetSpecificLayerName(Resource):
    """
    This endpoint returns a url link.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, category, name):
        """
        Returns a url link.
        """
        layer = db.get_specific_layer(category)
        if layer is None:
            raise (wz.NotFound("layers db not found."))
        else:
            return layer[0][name]


@api.route('/layers/create/<category>/<name>/<link>')
class CreateLayer(Resource):
    """
    This class supports adding a layer.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'duplicate key/invalid category')
    def post(self, category, name, link):
        """
        This method adds a layer to the layer db.
        """
        if category not in db.get_layers_as_list():
            raise (wz.NotAcceptable(f"{category} is not a valid category"))
        ret = db.add_layer(category, name, link)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("layer db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable(f"layer {name} already exists."))
        else:
            return f"{name} added."


@api.route('/rooms/create/<roomname>')
class CreateRoom(Resource):
    """
    This class supports adding a chat room.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, roomname):
        """
        This method adds a room to the room db.
        """
        ret = db.add_room(roomname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Chat room db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable(f"Chat room {roomname} already exists."))
        else:
            return f"{roomname} added."


@api.route('/rooms/delete/<roomname>')
class DeleteRoom(Resource):
    """
    This class enables deleting a chat room.
    While 'Forbidden` is a possible return value, we have not yet implemented
    a user privileges section, so it isn't used yet.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.FORBIDDEN,
                  'Only the owner of a room can delete it.')
    def post(self, roomname):
        """
        This method deletes a room from the room db.
        """
        ret = db.del_room(roomname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound(f"Chat room {roomname} not found."))
        else:
            return f"{roomname} deleted."


@api.route('/user/<username>')
class GetUser(Resource):
    """
    This endpoint returns a user.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Wrong Credentials')
    def get(self, username):
        user = db.get_specific_user(username)
        if user is None:
            raise (wz.NotFound("layers db not found."))
        else:
            return user


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    @api.response(HTTPStatus.OK, 'Success')
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}
