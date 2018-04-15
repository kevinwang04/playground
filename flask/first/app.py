#!/usr/bin/env python

from flask import Flask
from flask_restful import Api

errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
    'ServerInternalError': {
        'message': "Server Internal Error.",
        'status': 500,
    },
}

app = Flask(__name__)
api = Api(app,errors=errors)

from resources import TodoListResource,TodoResource
from resources import CategoryResource

api.add_resource(TodoListResource, '/todos', endpoint='todos')
api.add_resource(TodoResource, '/todos/<string:id>', endpoint='todo')
api.add_resource(CategoryResource, '/category')


class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]

app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3011, debug=False)