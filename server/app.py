#!/usr/bin/env python3

# Standard library imports

# Remote library imports

from flask import request, session, Blueprint, make_response, jsonify
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





@app.route("/")
def index():
    return "<h1>Project Server</h1>"


class Login(Resource):
    def post(self):
        data = request.get_json() if request.is_json else request.form
        if "username" not in data or "password" not in data:
            return {"error": "Missing required fields"}, 422
        user = User.query.filter_by(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            session["user_id"] = user.id
            return user.to_dict(), 200
        else:
            return {"error": "Invalid username or password"}, 401


class CheckSession(Resource):
    def get(self):
        if session["user_id"]:
            user = User.query.filter_by(id=session["user_id"]).first()
            return user.to_dict(), 200
        else:
            return {"error": "You are not logged in"}, 401


class Logout(Resource):
    def delete(self):
        if session["user_id"]:
            session["user_id"] = None
            return {}, 204
        else:
            return {"error": "You are not logged in"}, 401


class Signup(Resource):
    def post(self):
        data = request.get_json() if request.is_json else request.form
        if "username" not in data or "password" not in data:
            return {"error": "Missing required fields"}, 422
        try:
            user = User(
                username=data["username"],
            )
            user.set_password(data["password"])
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            return user.to_dict(), 201
        except Exception as e:
            print(e)
            return {"error": f"{str(e)}"}, 500

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

    def patch(self, id):
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

api.add_resource(ReviewList, '/reviews', endpoint='reviews')
api.add_resource(ReviewDetail, '/reviews/<int:id>', endpoint='review_detail')
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(Signup, "/signup", endpoint="signup")
if __name__ == "__main__":
    app.run(port=5555, debug=True)
