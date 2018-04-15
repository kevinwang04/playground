from models import Todo,Category
from db import session
from flask import Flask,request,abort
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
import json

# auto rollback

todo_fields = {
    'id': fields.Integer,
    'task': fields.String(attribute='name'),
    'uri': fields.Url('todo', absolute=True),
}

cate_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'sort': fields.String,
    'description': fields.String
}
parser = reqparse.RequestParser()
# category
parser_cate = parser.copy()
parser_cate.add_argument('name', type=str, required=True)
parser_cate.add_argument('sort', type=str, required=True)
parser_cate.add_argument('description', type=str, required=False)

class TodoResource(Resource):
    @marshal_with(todo_fields)
    def get(self, id):
        todo = session.query(Todo).filter(Todo.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))
        return todo

    def delete(self, id):
        todo = session.query(Todo).filter(Todo.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))
        session.delete(todo)
        session.commit()
        return {}, 204

    @marshal_with(todo_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        todo = session.query(Todo).filter(Todo.id == id).first()
        todo.task = parsed_args['task']
        session.add(todo)
        session.commit()
        return todo, 201
class TodoListResource(Resource):
    @marshal_with(todo_fields)
    def get(self):
        todos = session.query(Todo).all()
        return todos

    @marshal_with(todo_fields)
    def post(self):
        parsed_args = parser.parse_args()
        todo = Todo(task=parsed_args['task'])
        session.add(todo)
        session.commit()
        return todo, 201
class CategoryResource(Resource):
    @marshal_with(cate_fields)
    def post(self):
        req = request.get_json()
        args = json.dumps(parser_cate.parse_args(request))
        cate = Category(name=req['name'],sort=req['sort'],description=req['description'])
        try:
            session.add(cate)
            session.commit()
        except:
            session.rollback()
            abort(500)
        
        return cate, 201
        
    @marshal_with(cate_fields)
    def get(self):
        cates = session.query(Category).all()
        return cates