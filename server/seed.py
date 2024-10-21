#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import (
    db,
    User,
    Profile,
    UserActivity,
    Review,
    Activity,
    Site,
    SiteActivity,
    Location,
)

if __name__ == "__main__":
    fake = Faker()

    with app.app_context():
        print("Starting seed...")

        # Drop all existing data
        db.session.query(SiteActivity).delete()
        db.session.query(UserActivity).delete()
        db.session.query(Review).delete()
        db.session.query(Site).delete()
        db.session.query(Activity).delete()
        db.session.query(Profile).delete()
        db.session.query(User).delete()
        db.session.query(Location).delete()

        # Commit deletions
        db.session.commit()

        # SEED LOCATIONS
        locations = []
        for _ in range(5):
            location = Location(
                name=fake.city(),
                image="https://picsum.photos/500/300",
                description=fake.text(),
            )
            locations.append(location)
            db.session.add(location)

        db.session.commit()

        # SEED USERS AND PROFILES
        users = []
        profiles = []
        for _ in range(5):
            user = User(
                username=fake.user_name(),
            )
            user.set_password(fake.password())

            profile = Profile(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                image=fake.image_url(),
                bio=fake.text(),
                phone_number=fake.phone_number(),
                user=user,
            )

            users.append(user)
            profiles.append(profile)
            db.session.add(user)
            db.session.add(profile)
        test_user = User(username="markbkiunga")
        test_user.set_password("markbkiungapassword")
        db.session.add(test_user)

        db.session.commit()

        # SEED SITES
        sites = []
        for _ in range(5):
            site = Site(
                name=fake.company(),
                image='https://picsum.photos/100/100',
                description=fake.text(),
                is_saved=False,
                category=rc(["Historical", "Adventure", "Leisure"]),
                location=rc(locations),
            )
            sites.append(site)
            db.session.add(site)

        db.session.commit()

        # SEED ACTIVITIES
        activities = []
        for _ in range(5):
            activity = Activity(
                description=fake.sentence(),
                name=rc(["Hiking", "Kayaking", "Museum Tour", "Beach Day", "Safari"]),
                category=rc(["Outdoor", "Cultural", "Adventure"]),
            )
            activities.append(activity)
            db.session.add(activity)

        db.session.commit()

        # SEED USER ACTIVITIES
        for _ in range(5):
            user_activity = UserActivity(
                feedback=fake.text(),
                participation_date=fake.date_time_this_year(),
                user=rc(users),
                activity=rc(activities),
            )
            db.session.add(user_activity)

        db.session.commit()

        # SEED SITE ACTIVITIES
        for _ in range(5):
            site_activity = SiteActivity(activity=rc(activities), site=rc(sites))
            db.session.add(site_activity)

        db.session.commit()

        # SEED REVIEWS
        for _ in range(5):
            review = Review(
                description=fake.text(),
                rating=randint(1, 10),
                user=rc(users),
                site=rc(sites),
            )
            db.session.add(review)

        db.session.commit()

        print("Seeding complete!")
