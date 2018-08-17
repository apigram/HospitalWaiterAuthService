from flask_restful import Resource, fields, marshal, reqparse
from flask import g, abort
from app import basic_auth, auth, db
from app.models import User
import bcrypt

user_fields = {
    "uri": fields.Url('user'),
    "username": fields.String,
    "email": fields.String,
    "patient_id": fields.Integer,
}

authenticated_user_fields = {
    "uri": fields.Url('user'),
    "username": fields.String,
    "email": fields.String,
    "patient_id": fields.Integer,
    "token": fields.String
}


@basic_auth.verify_password
def verify_password(username, password):
    # first try to authenticate by token
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


class TokenResource(Resource):
    decorators = [auth.login_required]

    def get(self):
        user = {
            'id': g.user.id,
            'username': g.user.username,
            'email': g.user.email,
            'patient_id': g.user.patient_id,
            'token': g.user.generate_auth_token().decode('ascii')
        }
        return {"user": marshal(user, authenticated_user_fields)}


class UserResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')
        self.reqparse.add_argument('password_confirm', type=str, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        super(UserResource, self).__init__()

    def get(self, id):
        user = User.query.get_or_404(id)
        return {"user": marshal(user, user_fields)}

    def patch(self, id):
        args = self.reqparse.parse_args()
        user = User.query.get_or_404(id)
        if args['username'] is not None:
            user.username = args['username']
        if args['email'] is not None:
            user.email = args['email']
        if args['password'] is not None and args['password_confirm'] is not None:
            if args['password'] == args['password_confirm']:
                user.password = bcrypt.hashpw(args['password'].encode('utf8'), bcrypt.gensalt(10))
            else:
                abort(400)
        db.session.commit()
        return {"user": marshal(user, user_fields)}

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"result": True, "id": id}


class UserListResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')
        self.reqparse.add_argument('password_confirm', type=str, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        super(UserListResource, self).__init__()

    def get(self):
        users = User.query.all()
        return {"users": marshal([user for user in users], user_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        user = User()
        user.username = args['username']
        user.email = args['email']
        if args['password'] is None or args['password_confirm'] is None:
            abort(400)
        if args['password'] == args['password_confirm']:
            user.password = bcrypt.hashpw(args['password'].encode('utf8'), bcrypt.gensalt(10))
        else:
            abort(400)
        db.session.add(user)
        db.session.commit()
        return {"user": marshal(user, user_fields)}, 201
