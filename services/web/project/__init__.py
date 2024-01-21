import os, time
import requests
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_cors import CORS
from project.routes import *
from project.dataProcessing import *

app = Flask(__name__)
app.register_blueprint(api)
CORS(app)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email



