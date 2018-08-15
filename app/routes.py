from app import app
from flask_restful import Api

from app.resources.auth import TokenResource

api = Api(app)

# Token resource
api.add_resource(TokenResource, '/authservice/token', endpoint='auth_token')
