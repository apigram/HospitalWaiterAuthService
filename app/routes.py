from app import app
from flask_restful import Api

from app.resources.auth import UserResource, UserListResource, TokenResource

api = Api(app)

# Token resource
api.add_resource(TokenResource, '/authservice/token', endpoint='auth_token')

# User resources
api.add_resource(UserListResource, '/authservice/user', endpoint='users')
api.add_resource(UserResource, '/authservice/user/<int:id>', endpoint='user')
