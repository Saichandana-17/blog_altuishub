from flask_restful import Resource, reqparse
from models import User
from app import db

class UserRegisterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Username is required")
    parser.add_argument('password', type=str, required=True, help="Password is required")

    def post(self):
        data = UserRegisterResource.parser.parse_args()
        if User.query.filter_by(username=data['username']).first():
            return {"message": "User already exists"}, 400

        user = User(username=data['username'], password=data['password'])
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}, 201
