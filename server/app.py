#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, Blueprint, make_response, jsonify
from flask_restful import Resource, Api, reqparse

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Profile, UserActivity, Review, SiteActivity, Site, Location, Activity

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
import pytz

from sqlalchemy.exc import IntegrityError

gmt_plus_3 = pytz.timezone("Africa/Nairobi")

#initializing Flask-Restful Api


#defining resource classes

class index(Resource):
    def get(self):
        return make_response(jsonify({"message": "Welcome to Safiri API"}), 200)
    






if __name__ == '__main__':
    app.run(port=5555, debug=True)

