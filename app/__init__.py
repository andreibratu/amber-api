import os
from datetime import timedelta
from logging.handlers import RotatingFileHandler

from flask import Flask, logging
from app.config import Config
from app.extensions import db, migrate, jwt
from services.SecurityService import SecurityService
from flask_jwt import JWT
from app.encoder import Encoder


# Dependencies for app have been initialized in extensions.py in order to avoid import loop
def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def create_app(config_object=Config):
    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = os.environ.get('secret')
    flask_app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=2629744)
    flask_app.config.from_object(config_object)
    flask_app.json_encoder = Encoder
    register_extensions(flask_app)

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/ember.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Ember startup')

    return flask_app


app = create_app()
jwt = JWT(app=app, authentication_handler=SecurityService.authenticate, identity_handler=SecurityService.identity)

# import needed for SQLAlchemy to recognise the models
from app import models
# import needed for making the routes accessible
from controllers import UserController, EventController

app.run(threaded=True)