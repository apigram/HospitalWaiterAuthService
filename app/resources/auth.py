from flask_restful import Resource, fields
from flask import jsonify, g
from app import auth
from app.models import User

user_fields = {
    "username": fields.String,
    "patient": fields.Url('patient'),
    "token": fields.String
}


@auth.verify_password
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
            'patient_id': g.user.patient_id,
            'token': g.user.generate_auth_token().decode('ascii')
        }
        return jsonify({'user': user})
