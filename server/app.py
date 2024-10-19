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

class Index(Resource):
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

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username is required")
        parser.add_argument('password', required=True, help="Password is required")
        data = parser.parse_args()

        user = User.query.filter_by(username=data['username']).first()

        if user and user.check_password(data['password']):
            return make_response(jsonify(user.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "Invalid username or password"}), 401)

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

        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('bio', type=str)
        parser.add_argument('phone_number', type=str)
        data = parser.parse_args()

        profile = user.profile

        # Update profile fields
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
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        try:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": "User deleted successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)
        

class ReviewList(Resource):
    def get(self):
        reviews = Review.query.all()
        return jsonify([review.to_dict() for review in reviews])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('description', required=True, help="Description is required")
        parser.add_argument('rating', type=int, required=True, help="Rating is required")
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('site_id', type=int, required=True)
        data = parser.parse_args()

        user = User.query.get(data['user_id'])
        site = Site.query.get(data['site_id'])

        if not user or not site:
            return jsonify({"error": "User or Site not found"}), 404

        new_review = Review(
            description=data['description'],
            rating=data['rating'],
            user_id=user.id,
            site_id=site.id,
            created_at=datetime.now(gmt_plus_3),
            updated_at=datetime.now(gmt_plus_3)
        )

        try:
            db.session.add(new_review)
            db.session.commit()
            return jsonify(new_review.to_dict()), 201
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

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

        parser = reqparse.RequestParser()
        parser.add_argument('description', type=str)
        parser.add_argument('rating', type=int)
        data = parser.parse_args()

        review.description = data.get('description', review.description)
        review.rating = data.get('rating', review.rating)
        review.updated_at = datetime.now(gmt_plus_3)

        try:
            db.session.commit()
            return jsonify(review.to_dict())
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    def delete(self, id):
        review = Review.query.get(id)
        if not review:
            return jsonify({"error": "Review not found"}), 404

        try:
            db.session.delete(review)
            db.session.commit()
            return jsonify({"message": "Review deleted successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

api.add_resource(Index, '/')
api.add_resource(UserRegistration, '/users/register')
api.add_resource(UserLogin, '/users/login')
api.add_resource(UserDetail, '/users/<int:user_id>')
api.add_resource(ReviewList, '/reviews')
api.add_resource(ReviewDetail, '/reviews/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

