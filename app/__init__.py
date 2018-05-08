import os
from datetime import timedelta

from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, cors
from services.SecurityService import SecurityService
from flask_jwt import JWT
from app.encoder import Encoder


# Dependencies for app have been initialized in extensions.py in order to avoid import loop
def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)


def create_app(config_object=Config):
    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = os.environ.get('secret')
    flask_app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=2629744)
    flask_app.config.from_object(config_object)
    flask_app.json_encoder = Encoder
    register_extensions(flask_app)

    return flask_app


app = create_app()
jwt = JWT(app=app, authentication_handler=SecurityService.authenticate, identity_handler=SecurityService.identity)

# import needed for SQLAlchemy to recognise the models
from app import models
# import needed for making the routes accessible
from resources import UserResource, EventResource, InterestResource

print(os.environ.get('PORT'))
app.run(port=int(os.environ.get('PORT')), host='0.0.0.0')
