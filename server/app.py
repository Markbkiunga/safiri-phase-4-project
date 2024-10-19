#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, Blueprint, make_response, jsonify
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Profile, UserActivity, Review, SiteActivity, Site, Location, Activity

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
import pytz

from sqlalchemy.exc import IntegrityError

gmt_plus_3 = pytz.timezone("Africa/Nairobi")


user_blueprint = Blueprint('user', __name__)
review_bp = Blueprint('review', __name__)
activity_bp = Blueprint('activity', __name__)
site_bp = Blueprint('site', __name__)

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

# User registration route
@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return make_response(jsonify({"error": "Username and password are required"}), 400)
    
    if User.query.filter_by(username=username).first():
        return make_response(jsonify({"error": "Username already exists"}), 400)
    
    new_user = User(username=username)
    new_user.set_password(password)
    
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
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        return make_response(jsonify(user.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Invalid username or password"}), 401)

# Get user details
@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)
    
    return make_response(jsonify(user.to_dict()), 200)

# Fetch all users
@user_blueprint.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return make_response(jsonify([user.to_dict() for user in users]), 200)

# Update user profile
@user_blueprint.route('/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)
    
    data = request.get_json()
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

# Delete a user
@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
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

# Route to fetch all reviews
@review_bp.route('/', methods=['GET'])  
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews]), 200

# Route to fetch a specific review by its ID
@review_bp.route('/<int:id>', methods=['GET'])  
def get_review(id):
    review = Review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(review.to_dict()), 200

# Route to create a new review
@review_bp.route('/', methods=['POST'])  
def create_review():
    data = request.get_json()
    try:
        # Check if user and site exist
        user = User.query.get(data.get('user_id'))
        site = Site.query.get(data.get('site_id'))

        if not user or not site:
            return jsonify({"error": "User or Site not found"}), 404

        # Create the new review
        new_review = Review(
            description=data['description'],
            rating=data['rating'],
            user_id=user.id,
            site_id=site.id,
            created_at=datetime.now(gmt_plus_3),
            updated_at=datetime.now(gmt_plus_3)
        )
        db.session.add(new_review)
        db.session.commit()

        return jsonify(new_review.to_dict()), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

# Route to update a review
@review_bp.route('/<int:id>', methods=['PUT'])  
def update_review(id):
    review = Review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    data = request.get_json()
    try:
        # Update the review details
        review.description = data.get('description', review.description)
        review.rating = data.get('rating', review.rating)
        review.updated_at = datetime.now(gmt_plus_3)

        db.session.commit()
        return jsonify(review.to_dict()), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Route to delete a review
@review_bp.route('/<int:id>', methods=['DELETE']) 
def delete_review(id):
    review = Review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    try:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": "Review deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Route to fetch all activities
@activity_bp.route('/', methods=['GET'])
def get_all_activities():
    activities = Activity.query.all()
    return make_response(jsonify([activity.to_dict() for activity in activities]), 200)

# Route to fetch a specific activity by its ID
@activity_bp.route('/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity:
        return make_response(jsonify({"error": "Activity not found"}), 404)
    return make_response(jsonify(activity.to_dict()), 200)

# Route to create a new activity
@activity_bp.route('/', methods=['POST'])
def create_activity():
    data = request.get_json()
    try:
        new_activity = Activity(
            name=data['name'],
            description=data.get('description', ''),
            category=data.get('category', '')
        )
        db.session.add(new_activity)
        db.session.commit()
        return make_response(jsonify(new_activity.to_dict()), 201)
    except IntegrityError as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)
    except KeyError as e:
        return make_response(jsonify({"error": f"Missing field: {str(e)}"}), 400)

# Route to update an activity
@activity_bp.route('/<int:activity_id>', methods=['PUT'])
def update_activity(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity:
        return make_response(jsonify({"error": "Activity not found"}), 404)

    data = request.get_json()
    try:
        activity.name = data.get('name', activity.name)
        activity.description = data.get('description', activity.description)
        activity.category = data.get('category', activity.category)

        db.session.commit()
        return make_response(jsonify(activity.to_dict()), 200)
    except IntegrityError as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)

# Route to delete an activity
@activity_bp.route('/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity:
        return make_response(jsonify({"error": "Activity not found"}), 404)

    try:
        db.session.delete(activity)
        db.session.commit()
        return make_response(jsonify({"message": "Activity deleted successfully"}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
    
# Route to fetch all sites
@site_bp.route('/', methods=['GET'])
def get_all_sites():
    sites = Site.query.all()
    return make_response(jsonify([site.to_dict() for site in sites]), 200)

# Route to fetch a specific site by its ID
@site_bp.route('/<int:site_id>', methods=['GET'])
def get_site(site_id):
    site = Site.query.get(site_id)
    if not site:
        return make_response(jsonify({"error": "Site not found"}), 404)
    return make_response(jsonify(site.to_dict()), 200)

# Route to create a new site
@site_bp.route('/', methods=['POST'])
def create_site():
    data = request.get_json()
    try:
        new_site = Site(
            name=data['name'],
            description=data.get('description', ''),
            image=data.get('image', ''),
            category=data.get('category', ''),
            location_id=data['location_id']  
        )
        db.session.add(new_site)
        db.session.commit()
        return make_response(jsonify(new_site.to_dict()), 201)
    except IntegrityError as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)
    except KeyError as e:
        return make_response(jsonify({"error": f"Missing field: {str(e)}"}), 400)

# Route to update a site
@site_bp.route('/<int:site_id>', methods=['PUT'])
def update_site(site_id):
    site = Site.query.get(site_id)
    if not site:
        return make_response(jsonify({"error": "Site not found"}), 404)

    data = request.get_json()
    try:
        site.name = data.get('name', site.name)
        site.description = data.get('description', site.description)
        site.image = data.get('image', site.image)
        site.category = data.get('category', site.category)
        site.is_saved = data.get('is_saved', site.is_saved)
        site.location_id = data.get('location_id', site.location_id)

        db.session.commit()
        return make_response(jsonify(site.to_dict()), 200)
    except IntegrityError as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)

# Route to delete a site
@site_bp.route('/<int:site_id>', methods=['DELETE'])
def delete_site(site_id):
    site = Site.query.get(site_id)
    if not site:
        return make_response(jsonify({"error": "Site not found"}), 404)

    try:
        db.session.delete(site)
        db.session.commit()
        return make_response(jsonify({"message": "Site deleted successfully"}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)



app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(review_bp, url_prefix='/reviews')
app.register_blueprint(activity_bp, url_prefix='/activities')
app.register_blueprint(site_bp, url_prefix='/sites')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

