#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, Blueprint, make_response, jsonify
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Profile, UserActivity, Review, SiteActivity, Site, Location

from werkzeug.security import generate_password_hash, check_password_hash


user_blueprint = Blueprint('user', __name__)

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

# User registration route
@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    # Validate required fields
    if not username or not password:
        return make_response(jsonify({"error": "Username and password are required"}), 400)
    
    # Check if the username is already taken
    if User.query.filter_by(username=username).first():
        return make_response(jsonify({"error": "Username already exists"}), 400)
    
    # Create new user and hash the password
    new_user = User(username=username)
    new_user.set_password(password)
    
    # Create a default profile for the user
    profile_data = data.get('profile', {})
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

# User login route
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Find the user by username
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        return make_response(jsonify(user.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Invalid username or password"}), 401)

# Update user profile
@user_blueprint.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)
    
    data = request.get_json()
    profile = user.profile
    
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

# Get user details
@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)
    
    return make_response(jsonify(user.to_dict()), 200)

# Delete a user
@user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
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





if __name__ == '__main__':
    app.run(port=5555, debug=True)

