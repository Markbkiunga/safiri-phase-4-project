from datetime import datetime
import pytz
from sqlalchemy import DateTime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from config import db
gmt_plus_3 = pytz.timezone("Africa/Nairobi")

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-user_activities.user','-activities.users', '-reviews.user', '-profile.user') 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column( 
            DateTime(timezone=True),
            server_default=db.func.now(),
            default=datetime.now(gmt_plus_3),)
    updated_at = db.Column(
        DateTime(timezone=True),
        onupdate=datetime.now(gmt_plus_3),
        default=datetime.now(gmt_plus_3),)

    user_activities = db.relationship('UserActivity', back_populates='user', cascade="all, delete-orphan")
    activities = association_proxy('user_activities', 'activity', creator=lambda activity_obj: UserActivity(activity = activity_obj))
    sites = association_proxy('reviews', 'site', creator=lambda site_obj: Review(site = site_obj))

    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")
    profile = db.relationship('Profile', uselist=False, back_populates='user', cascade='all, delete-orphan')

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 5:
            raise ValueError('Username must be at least 5 characters long')
        return username

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    

class Profile(db.Model, SerializerMixin):
    __tablename__ = 'profiles'
    serialize_rules = ('-user.profile',)
    
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
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError('Email should contain @')
        return email


class UserActivity(db.Model, SerializerMixin):
    __tablename__ = 'user_activities'
    serialize_rules = ('-user.user_activities', '-activity.user_activities',)
    
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.Text)
    participation_date = db.Column(DateTime(timezone=True), nullable=False)
    created_at = db.Column(
            DateTime(timezone=True),
            server_default=db.func.now(),
            default=datetime.now(gmt_plus_3),)
    updated_at = db.Column(
        DateTime(timezone=True),
        onupdate=datetime.now(gmt_plus_3),
        default=datetime.now(gmt_plus_3),)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)

    user = db.relationship('User', back_populates='user_activities')
    activity = db.relationship('Activity', back_populates='user_activities')

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    serialize_rules = ('-user.reviews', '-site.reviews',)

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
            DateTime(timezone=True),
            server_default=db.func.now(),
            default=datetime.now(gmt_plus_3),)
    updated_at = db.Column(
        DateTime(timezone=True),
        onupdate=datetime.now(gmt_plus_3),
        default=datetime.now(gmt_plus_3),)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)

    user = db.relationship('User', back_populates='reviews')
    site = db.relationship('Site', back_populates='reviews')

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 10):
            raise ValueError('Rating must be between 1 and 10')
        return value

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'
    serialize_rules = ('-user_activities.activity','-users.activities', '-site_activities.activity',)
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    created_at = db.Column( 
            DateTime(timezone=True),
            server_default=db.func.now(),
            default=datetime.now(gmt_plus_3),)
    updated_at = db.Column(
        DateTime(timezone=True),
        onupdate=datetime.now(gmt_plus_3),
        default=datetime.now(gmt_plus_3),)
    
    user_activities = db.relationship('UserActivity', back_populates='activity', cascade='all, delete-orphan')
    users = association_proxy("user_activities", "user", creator=lambda user_obj: UserActivity(user = user_obj))

    site_activities = db.relationship('SiteActivity', back_populates='activity', cascade='all, delete-orphan')


class SiteActivity(db.Model):
    __tablename__ = 'site_activities'
    serialize_rules = ('-site.site_activities','-activity.site_activities',)
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column( 
            DateTime(timezone=True),
            server_default=db.func.now(),
            default=datetime.now(gmt_plus_3),)
    updated_at = db.Column(
        DateTime(timezone=True),
        onupdate=datetime.now(gmt_plus_3),
        default=datetime.now(gmt_plus_3),)
    
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)

    activity = db.relationship('Activity', back_populates='site_activities')
    site = db.relationship('Site', back_populates='site_activities')


class Site(db.Model, SerializerMixin):
    __tablename__ = 'sites'
    serialize_rules = ('-site_activities.site','-reviews.site', '-location.sites', '-users.sites',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    is_saved = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50))

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    
    site_activities = db.relationship('SiteActivity', back_populates='site', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='site', cascade='all, delete-orphan')
    location = db.relationship('Location', back_populates='sites')

    users = association_proxy('reviews', 'user', creator=lambda user_obj: Review(user= user_obj))


class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'
    serialize_rules = ('-sites.location',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(
            DateTime(timezone=True),
            server_default=db.func.now(),
            default=datetime.now(gmt_plus_3),)
    updated_at = db.Column(
        DateTime(timezone=True),
        onupdate=datetime.now(gmt_plus_3),
        default=datetime.now(gmt_plus_3),)

    sites = db.relationship('Site', back_populates='location', cascade='all, delete-orphan')