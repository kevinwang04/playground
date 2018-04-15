from flask import Flask,request
from flask_restful import reqparse,Resource, Api,fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import json
parser = reqparse.RequestParser()
parser.add_argument('todo_id', type=str)
# 0.10.1

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'Fianna'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kevin@mysql@localhost:3306/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
def init_db():
    db.create_all()

todos_fields = {
    'name':   fields.String,
    'todo_id': fields.String(attribute='id')

}
class Todos(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False, server_default='', unique=True)
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False, unique=True, server_default='', index=True)
    role_id = db.Column(db.Integer, nullable=False, server_default='0')
    def __repr__(self): # 用于打印的
        return '<User %r,Role id %r>' %(self.username,self.role_id)


class TodoSimple(Resource):
    @marshal_with(todos_fields)
    def get(self):
        todos = Todos.query.all()
        return todos
    def post(self):
        args = parser.parse_args()
        db.session.add(Todos(name=args['todo_id']))
        db.session.commit()
        return {'todo_id': args['todo_id']}

api.add_resource(TodoSimple, '/todos')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)