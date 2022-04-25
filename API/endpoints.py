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


@api.route('/user/<username>/<password>')
class CheckCredentials(Resource):
    """
    This endpoint returns a user.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Wrong Credentials')
    def get(self, username, password):
        ret = db.check_credentials(username, password)
        return ret


@api.route('/user/register/<username>/<password>')
class Register(Resource):
    """
    This endpoint adds a new user to the database
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Duplicate Username')
    def post(self, username, password):
        ret = db.add_user(username, password)
        if ret == db.DUPLICATE:
            raise (wz.NotAcceptable(f"{username} already exists."))
        return f"{username} added."


@api.route('/scribbles/create/<username>/<body>/<head>/<eyes>/<mouth>')
class CreateScribble(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def post(self, username, body, head, eyes, mouth):
        ret = db.add_scribble(username, body, head, eyes, mouth)
        if ret == db.DUPLICATE:
            raise (wz.NotAcceptable("Scribble already exists."))
        elif ret == db.OK:
            return f"{username} added a new Scribble."


@api.route('/scribbles/<username>')
class GetScribbles(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Invalid Username')
    def get(self, username):
        scribbles = db.get_scribbles(username)
        if scribbles == []:
            raise (wz.NotAcceptable(f"{username} does not exist."))
        else:
            return scribbles


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
