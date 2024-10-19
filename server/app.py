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

# Simple index page to verify server is running
class Index(Resource):
    def get(self):
        return '<h1>Project Server Running</h1>'

# User registration class
class UserRegistration(Resource):
    def post(self):
        # Create a parser to get the input data
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username is required")
        parser.add_argument('password', required=True, help="Password is required")
        parser.add_argument('profile', type=dict, location='json') 
        data = parser.parse_args()

        # Extract data from the parser
        username = data['username']
        password = data['password']
        profile_data = data.get('profile', {})

        # Check if the username already exists in the database
        if User.query.filter_by(username=username).first():
            return make_response(jsonify({"error": "Username already exists"}), 400)

        # Create a new user and hash their password
        new_user = User(username=username)
        new_user.set_password(password)

        # Create a new profile for the user
        profile = Profile(
            first_name=profile_data.get('first_name', ''),
            last_name=profile_data.get('last_name', ''),
            email=profile_data.get('email', ''),
            bio=profile_data.get('bio', ''),
            phone_number=profile_data.get('phone_number', ''),
            user=new_user  
        )

        # Add the new user and profile to the database
        db.session.add(new_user)
        db.session.add(profile)
        db.session.commit()

        # Return the created user data
        return make_response(jsonify(new_user.to_dict()), 201)

# User login class
class UserLogin(Resource):
    def post(self):
        # Parse the input data
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username is required")
        parser.add_argument('password', required=True, help="Password is required")
        data = parser.parse_args()

        # Check if the user exists
        user = User.query.filter_by(username=data['username']).first()

        # If the user exists and the password is correct, return the user info
        if user and user.check_password(data['password']):
            return make_response(jsonify(user.to_dict()), 200)
        else:
            # If login fails, return an error message
            return make_response(jsonify({"error": "Invalid username or password"}), 401)

# Class to get, update, or delete a specific user by ID
class UserDetail(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
        return make_response(jsonify(user.to_dict()), 200)

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        # Parse input data to update user profile
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('bio', type=str)
        parser.add_argument('phone_number', type=str)
        data = parser.parse_args()

        # Update the profile with the new data
        profile = user.profile
        profile.first_name = data.get('first_name', profile.first_name)
        profile.last_name = data.get('last_name', profile.last_name)
        profile.email = data.get('email', profile.email)
        profile.bio = data.get('bio', profile.bio)
        profile.phone_number = data.get('phone_number', profile.phone_number)

        # Save the updated profile
        db.session.commit()
        return make_response(jsonify(profile.to_dict()), 200)

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted successfully"}), 200)

# Class to get and create reviews
class ReviewList(Resource):
    def get(self):
        # Get all reviews
        reviews = Review.query.all()
        return jsonify([review.to_dict() for review in reviews])

    def post(self):
        # Parse input data
        parser = reqparse.RequestParser()
        parser.add_argument('description', required=True, help="Description is required")
        parser.add_argument('rating', type=int, required=True, help="Rating is required")
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('site_id', type=int, required=True)
        data = parser.parse_args()

        # Check if user and site exist
        user = User.query.get(data['user_id'])
        site = Site.query.get(data['site_id'])

        if not user or not site:
            return jsonify({"error": "User or Site not found"}), 404

        # Create a new review
        new_review = Review(
            description=data['description'],
            rating=data['rating'],
            user_id=user.id,
            site_id=site.id,
            created_at=datetime.now(gmt_plus_3)
        )

        # Save the review in the database
        db.session.add(new_review)
        db.session.commit()
        return jsonify(new_review.to_dict()), 201

# Class to handle individual review actions
class ReviewDetail(Resource):
    def get(self, id):
        review = Review.query.get(id)
        if not review:
            return jsonify({"error": "Review not found"}), 404
        return jsonify(review.to_dict())

    def put(self, id):
        review = Review.query.get(id)
        if not review:
            return jsonify({"error": "Review not found"}), 404

        # Parse input data to update review
        parser = reqparse.RequestParser()
        parser.add_argument('description', type=str)
        parser.add_argument('rating', type=int)
        data = parser.parse_args()

        review.description = data.get('description', review.description)
        review.rating = data.get('rating', review.rating)
        review.updated_at = datetime.now(gmt_plus_3)

        db.session.commit()
        return jsonify(review.to_dict())

    def delete(self, id):
        review = Review.query.get(id)
        if not review:
            return jsonify({"error": "Review not found"}), 404

        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": "Review deleted successfully"})
    
# Profile Resource
class ProfileDetail(Resource):
    def get(self, user_id):
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            return make_response(jsonify({"error": "Profile not found"}), 404)
        return make_response(jsonify(profile.to_dict()), 200)

    def put(self, user_id):
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            return make_response(jsonify({"error": "Profile not found"}), 404)

        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('bio', type=str)
        parser.add_argument('phone_number', type=str)
        data = parser.parse_args()

        profile.first_name = data.get('first_name', profile.first_name)
        profile.last_name = data.get('last_name', profile.last_name)
        profile.email = data.get('email', profile.email)
        profile.bio = data.get('bio', profile.bio)
        profile.phone_number = data.get('phone_number', profile.phone_number)

        try:
            db.session.commit()
            return make_response(jsonify(profile.to_dict()), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)

    def delete(self, user_id):
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            return make_response(jsonify({"error": "Profile not found"}), 404)

        try:
            db.session.delete(profile)
            db.session.commit()
            return make_response(jsonify({"message": "Profile deleted successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)
        
# Activity Resource
class ActivityList(Resource):
    def get(self):
        activities = Activity.query.all()
        return jsonify([activity.to_dict() for activity in activities])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="Name is required")
        parser.add_argument('description', type=str)
        parser.add_argument('category', type=str)
        data = parser.parse_args()

        new_activity = Activity(
            name=data['name'],
            description=data.get('description', ''),
            category=data.get('category', ''),
            created_at=datetime.now(gmt_plus_3),
            updated_at=datetime.now(gmt_plus_3)
        )

        try:
            db.session.add(new_activity)
            db.session.commit()
            return jsonify(new_activity.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

class ActivityDetail(Resource):
    def get(self, id):
        activity = Activity.query.get(id)
        if not activity:
            return jsonify({"error": "Activity not found"}), 404
        return jsonify(activity.to_dict())

    def put(self, id):
        activity = Activity.query.get(id)
        if not activity:
            return jsonify({"error": "Activity not found"}), 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('category', type=str)
        data = parser.parse_args()

        activity.name = data.get('name', activity.name)
        activity.description = data.get('description', activity.description)
        activity.category = data.get('category', activity.category)
        activity.updated_at = datetime.now(gmt_plus_3)

        try:
            db.session.commit()
            return jsonify(activity.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def delete(self, id):
        activity = Activity.query.get(id)
        if not activity:
            return jsonify({"error": "Activity not found"}), 404

        try:
            db.session.delete(activity)
            db.session.commit()
            return jsonify({"message": "Activity deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


api.add_resource(Index, '/')
api.add_resource(UserRegistration, '/users/register')
api.add_resource(UserLogin, '/users/login')
api.add_resource(UserDetail, '/users/<int:user_id>')
api.add_resource(ReviewList, '/reviews')
api.add_resource(ReviewDetail, '/reviews/<int:id>')
api.add_resource(ProfileDetail, '/profiles/<int:user_id>')
api.add_resource(ActivityList, '/activities')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

