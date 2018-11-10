from flask import Flask
from sqlalchemy_utils import database_exists, create_database

from src import SQLALCHEMY_DATABASE_URI
from src.db.model import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    if not database_exists(db.engine.url):
        create_database(db.engine.url)
    db.create_all()
