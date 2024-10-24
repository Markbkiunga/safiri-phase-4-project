# Standard library imports
import os
from dotenv import load_dotenv

load_dotenv()

# Remote library imports
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_cors import CORS

# Local imports

# Instantiate app, set attributes
app = Flask(__name__)
CORS(
    app,
    origins=["https://safiri-phase-4-project.vercel.app"],
    supports_credentials=True,
)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.update(
    SESSION_COOKIE_SECURE=True,  # Ensure it's set to True for HTTPS
    SESSION_COOKIE_SAMESITE="Lax",  # Controls whether the session cookie is sent for cross-origin requests
    SESSION_COOKIE_HTTPONLY=True,  # Prevents client-side access to session cookies
)

app.json.compact = False

# Define metadata, instantiate db
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)
