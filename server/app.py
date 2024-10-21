#!/usr/bin/env python3

# Standard library imports

# Remote library imports

from flask import request, session, Blueprint, make_response, jsonify
from flask_restful import Resource, Api, reqparse

# Local imports
from config import app, db, api

# Add your model imports
from models import (
    User,
    Profile,
    UserActivity,
    Review,
    SiteActivity,
    Site,
    Location,
    Activity,
)

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
import pytz


from sqlalchemy.exc import IntegrityError

gmt_plus_3 = pytz.timezone("Africa/Nairobi")

# initializing Flask-Restful Api


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


class UserList(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])


class UserDetail(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
        return make_response(jsonify(user.to_dict()), 200)

    def patch(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        # Parse input data to update user profile
        parser = reqparse.RequestParser()
        parser.add_argument("first_name", type=str)
        parser.add_argument("last_name", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("bio", type=str)
        parser.add_argument("phone_number", type=str)
        data = parser.parse_args()

        # Update the profile with the new data
        profile = user.profile
        profile.first_name = data.get("first_name", profile.first_name)
        profile.last_name = data.get("last_name", profile.last_name)
        profile.email = data.get("email", profile.email)
        profile.bio = data.get("bio", profile.bio)
        profile.phone_number = data.get("phone_number", profile.phone_number)

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
        if not session["user_id"]:
            print("User not logged in")
            return make_response({"error": "User not logged in"}, 401)

        # Parse input data
        parser = reqparse.RequestParser()
        parser.add_argument("reviewText", required=True, help="Description is required")
        parser.add_argument(
            "rating", type=int, required=True, help="Rating is required"
        )
        parser.add_argument("userId", type=int, required=True)
        parser.add_argument("siteId", type=int, required=True)
        data = parser.parse_args()

        # Check if user and site exist
        user = User.query.get(data["userId"])
        site = Site.query.get(data["siteId"])

        if not user or not site:
            return jsonify({"error": "User or Site not found"}), 404

        # Create a new review
        try:
            new_review = Review(
                description=data["reviewText"],
                rating=data["rating"],
                user_id=user.id,
                site_id=site.id,
                created_at=datetime.now(gmt_plus_3),
            )

            # Save the review in the database
            db.session.add(new_review)
            db.session.commit()
            return new_review.to_dict(), 201
        except Exception as e:
            print(e)
            return jsonify({"error": f"{e}"}), 500


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
        parser.add_argument("description", type=str)
        parser.add_argument("rating", type=int)
        data = parser.parse_args()

        review.description = data.get("description", review.description)
        review.rating = data.get("rating", review.rating)
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

    def patch(self, user_id):
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            return make_response(jsonify({"error": "Profile not found"}), 404)

        parser = reqparse.RequestParser()
        parser.add_argument("first_name", type=str)
        parser.add_argument("last_name", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("bio", type=str)
        parser.add_argument("phone_number", type=str)
        data = parser.parse_args()

        profile.first_name = data.get("first_name", profile.first_name)
        profile.last_name = data.get("last_name", profile.last_name)
        profile.email = data.get("email", profile.email)
        profile.bio = data.get("bio", profile.bio)
        profile.phone_number = data.get("phone_number", profile.phone_number)

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
            return make_response(
                jsonify({"message": "Profile deleted successfully"}), 200
            )
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
        parser.add_argument("name", required=True, help="Name is required")
        parser.add_argument("description", type=str)
        parser.add_argument("category", type=str)
        data = parser.parse_args()

        new_activity = Activity(
            name=data["name"],
            description=data.get("description", ""),
            category=data.get("category", ""),
            created_at=datetime.now(gmt_plus_3),
            updated_at=datetime.now(gmt_plus_3),
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

    def patch(self, id):
        activity = Activity.query.get(id)
        if not activity:
            return jsonify({"error": "Activity not found"}), 404

        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("description", type=str)
        parser.add_argument("category", type=str)
        data = parser.parse_args()

        activity.name = data.get("name", activity.name)
        activity.description = data.get("description", activity.description)
        activity.category = data.get("category", activity.category)
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


# UserActivity Resource
class UserActivityList(Resource):
    def get(self):
        user_activities = UserActivity.query.all()
        return jsonify([user_activity.to_dict() for user_activity in user_activities])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", required=True, help="User ID is required")
        parser.add_argument(
            "activity_id", required=True, help="Activity ID is required"
        )
        parser.add_argument("feedback", type=str)
        parser.add_argument(
            "participation_date", type=str, default=str(datetime.now(gmt_plus_3))
        )
        data = parser.parse_args()

        new_user_activity = UserActivity(
            user_id=data["user_id"],
            activity_id=data["activity_id"],
            feedback=data.get("feedback", ""),
            participation_date=datetime.now(gmt_plus_3),
            created_at=datetime.now(gmt_plus_3),
            updated_at=datetime.now(gmt_plus_3),
        )

        try:
            db.session.add(new_user_activity)
            db.session.commit()
            return jsonify(new_user_activity.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


class UserActivityDetail(Resource):
    def get(self, id):
        user_activity = UserActivity.query.get(id)
        if not user_activity:
            return jsonify({"error": "User Activity not found"}), 404
        return jsonify(user_activity.to_dict())

    def patch(self, id):
        user_activity = UserActivity.query.get(id)
        if not user_activity:
            return jsonify({"error": "User Activity not found"}), 404

        parser = reqparse.RequestParser()
        parser.add_argument("feedback", type=str)
        data = parser.parse_args()

        user_activity.feedback = data.get("feedback", user_activity.feedback)
        user_activity.updated_at = datetime.now(gmt_plus_3)

        try:
            db.session.commit()
            return jsonify(user_activity.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def delete(self, id):
        user_activity = UserActivity.query.get(id)
        if not user_activity:
            return jsonify({"error": "User Activity not found"}), 404

        try:
            db.session.delete(user_activity)
            db.session.commit()
            return jsonify({"message": "User Activity deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


# Site Resource
class SiteList(Resource):
    def get(self):
        sites = Site.query.all()
        return jsonify([site.to_dict() for site in sites])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Name is required")
        parser.add_argument("description", type=str)
        parser.add_argument("category", type=str)
        parser.add_argument("location_id", type=int, required=True)
        data = parser.parse_args()

        new_site = Site(
            name=data["name"],
            description=data.get("description", ""),
            category=data.get("category", ""),
            location_id=data["location_id"],
        )

        try:
            db.session.add(new_site)
            db.session.commit()
            return jsonify(new_site.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


class SiteDetail(Resource):
    def get(self, id):
        site = Site.query.get(id)
        if not site:
            return jsonify({"error": "Site not found"}), 404
        return jsonify(site.to_dict())

    def patch(self, id):
        site = Site.query.get(id)
        if not site:
            return jsonify({"error": "Site not found"}), 404

        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("description", type=str)
        parser.add_argument("category", type=str)
        data = parser.parse_args()

        site.name = data.get("name", site.name)
        site.description = data.get("description", site.description)
        site.category = data.get("category", site.category)

        try:
            db.session.commit()
            return jsonify(site.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def delete(self, id):
        site = Site.query.get(id)
        if not site:
            return jsonify({"error": "Site not found"}), 404

        try:
            db.session.delete(site)
            db.session.commit()
            return jsonify({"message": "Site deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


def serialize_site_activity(site_activity):
    return {
        "id": site_activity.id,
        "activity_id": site_activity.activity_id,
        "site_id": site_activity.site_id,
        "created_at": (
            site_activity.created_at.isoformat() if site_activity.created_at else None
        ),
        "updated_at": (
            site_activity.updated_at.isoformat() if site_activity.updated_at else None
        ),
    }


class SiteActivityList(Resource):
    def get(self):
        site_activities = SiteActivity.query.all()
        return jsonify(
            [
                serialize_site_activity(site_activity)
                for site_activity in site_activities
            ]
        )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "activity_id", required=True, help="Activity ID is required"
        )
        parser.add_argument("site_id", required=True, help="Site ID is required")
        data = parser.parse_args()

        new_site_activity = SiteActivity(
            activity_id=data["activity_id"], site_id=data["site_id"]
        )

        try:
            db.session.add(new_site_activity)
            db.session.commit()
            return serialize_site_activity(new_site_activity), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


class SiteActivityDetail(Resource):
    def get(self, id):
        site_activity = SiteActivity.query.get(id)
        if not site_activity:
            return jsonify({"error": "SiteActivity not found"}), 404
        return jsonify(site_activity.to_dict())

    def patch(self, id):
        site_activity = SiteActivity.query.get(id)
        if not site_activity:
            return jsonify({"error": "SiteActivity not found"}), 404

        parser = reqparse.RequestParser()
        parser.add_argument("activity_id", type=int)
        parser.add_argument("site_id", type=int)
        data = parser.parse_args()

        if data["activity_id"] is not None:
            site_activity.activity_id = data["activity_id"]
        if data["site_id"] is not None:
            site_activity.site_id = data["site_id"]

        try:
            db.session.commit()
            return jsonify(site_activity.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def delete(self, id):
        site_activity = SiteActivity.query.get(id)
        if not site_activity:
            return jsonify({"error": "SiteActivity not found"}), 404

        try:
            db.session.delete(site_activity)
            db.session.commit()
            return jsonify({"message": "SiteActivity deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


# Location Resource
class LocationList(Resource):
    def get(self):
        locations = Location.query.all()
        return jsonify([location.to_dict() for location in locations])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Name is required")
        parser.add_argument("description", type=str)
        data = parser.parse_args()

        new_location = Location(
            name=data["name"], description=data.get("description", "")
        )

        try:
            db.session.add(new_location)
            db.session.commit()
            return jsonify(new_location.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


api.add_resource(Login, "/login", endpoint="login")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(UserDetail, "/users/<int:user_id>")
api.add_resource(ReviewList, "/reviews", endpoint="reviews")
api.add_resource(ReviewDetail, "/reviews/<int:id>", endpoint="review_detail")
api.add_resource(ProfileDetail, "/profiles/<int:user_id>")
api.add_resource(ActivityList, "/activities")
api.add_resource(ActivityDetail, "/activities/<int:id>")
api.add_resource(UserActivityList, "/user_activities")
api.add_resource(UserActivityDetail, "/user_activities/<int:id>")
api.add_resource(SiteList, "/sites")
api.add_resource(SiteDetail, "/sites/<int:id>")
api.add_resource(SiteActivityList, "/site_activities", endpoint="site_activities")
api.add_resource(SiteActivityDetail, "/site_activities/<int:id>")
api.add_resource(LocationList, "/locations")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
