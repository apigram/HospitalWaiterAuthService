from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")
cors = CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()

from app import routes
# Register RESTful web service routes
