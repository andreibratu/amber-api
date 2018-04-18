import os
from flask_jwt import JWT
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWT()
socketIO = SocketIO()
cors = CORS()