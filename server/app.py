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
    
class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username is required")
        parser.add_argument('password', required=True, help="Password is required")
        parser.add_argument('profile', type=dict, location='json')
        data = parser.parse_args()

        username = data['username']
        password = data['password']
        profile_data = data.get('profile', {})

        if User.query.filter_by(username=username).first():
            return make_response(jsonify({"error": "Username already exists"}), 400)

        new_user = User(username=username)
        new_user.set_password(password)
        
        profile = Profile(
            first_name=profile_data.get('first_name', ''),
            last_name=profile_data.get('last_name', ''),
            email=profile_data.get('email', ''),
            bio=profile_data.get('bio', ''),
            phone_number=profile_data.get('phone_number', ''),
            user=new_user
        )

        try:
            db.session.add(new_user)
            db.session.add(profile)
            db.session.commit()
            return make_response(jsonify(new_user.to_dict()), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)






if __name__ == '__main__':
    app.run(port=5555, debug=True)

