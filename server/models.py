from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_serialize import FlaskSerializeMixin



db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    activities = db.relationship('Activity', secondary='user_activities', back_populates='users')
    reviews = db.relationship('Review', back_populates='user')
    profile = db.relationship('Profile', uselist=False, back_populates='user', cascade='all, delete-orphan')

    @validates('username')
    def validate_username(self, key, value):
        if len(value) < 5:
            raise ValueError('Username must be at least 5 characters long')
        return value

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'profile': self.profile.serialize() if self.profile else None
        }


class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    image = db.Column(db.String(255))
    bio = db.Column(db.Text)
    phone_number = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='profile')


    @validates('email')
    def validate_email(self, key, value):
        if '@' not in value:
            raise ValueError('Invalid email format')
        return value

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'image': self.image,
            'bio': self.bio,
            'phone_number': self.phone_number
        }



class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.Text)
    participation_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)

    user = db.relationship('User', back_populates='activities')
    activity = db.relationship('Activity', back_populates='participants')

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)

    user = db.relationship('User', back_populates='reviews')
    site = db.relationship('Site', back_populates='reviews')

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError('Rating must be between 1 and 5')
        return value

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'rating': self.rating,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id
        }




class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    users = db.relationship('User', secondary='user_activities', back_populates='activities')
    participants = db.relationship('UserActivity', back_populates='activity')
    site_activities = db.relationship('SiteActivity', back_populates='activity', cascade='all, delete-orphan')


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }





class SiteActivity(db.Model):
    __tablename__ = 'site_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)

    activity = db.relationship('Activity', back_populates='site_activities')
    site = db.relationship('Site', back_populates='site_activities')


    



class Site(db.Model):
    __tablename__ = 'sites'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    is_saved = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    
    activities = db.relationship('Activity', secondary='site_activities', back_populates='site')
    reviews = db.relationship('Review', back_populates='site')
    location = db.relationship('Location', back_populates='sites')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'is_saved': self.is_saved,
            'activities': [activity.serialize() for activity in self.activities]
        }





class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    sites = db.relationship('Site', back_populates='location', cascade='all, delete-orphan')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


