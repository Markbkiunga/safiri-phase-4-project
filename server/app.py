#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, session
from flask_restful import Resource

# Local imports
from config import app, db, api

# Add your model imports
from models import User, Profile, UserActivity, Review, SiteActivity, Site, Location


# Views go here!


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


api.add_resource(Login, "/login", endpoint="login")
if __name__ == "__main__":
    app.run(port=5555, debug=True)
