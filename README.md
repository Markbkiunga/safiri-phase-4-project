# Safiri - Backend API

Welcome to the backend of the **Safiri** project, a travel platform where users can explore sites, participate in activities, and leave reviews. This backend API is built using Flask and SQLAlchemy, providing the core functionality to manage users, profiles, activities, reviews, sites, and more.

## Table of Contents

- [Project Setup](#project-setup)
- [Models](#models)
  - [User](#user)
  - [Profile](#profile)
  - [Review](#review)
  - [Activity](#activity)
  - [Site](#site)
  - [Location](#location)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Users](#users)
  - [Profiles](#profiles)
  - [Reviews](#reviews)
  - [Activities](#activities)
  - [Sites](#sites)
  - [Locations](#locations)
- [Database Setup](#database-setup)
- [Seeding Data](#seeding-data)

## Project Setup

To get started with the project, follow the steps below:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/safiri-backend.git
   cd safiri-backend
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the Environment Variables**:  
   Create a `.env` file at the root directory and configure the necessary environment variables, such as:
   ```env
   DB_URI=postgresql://username:password@localhost/safiri
   ```

5. **Run Database Migrations**:
   Initialize and migrate the database schema:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the Development Server**:
   ```bash
   flask run
   ```

## Models

### User

The `User` model represents a user in the system. It stores information such as:

- **username**: Unique and alphanumeric (must be at least 5 characters).
- **password**: Hashed using `werkzeug.security`.
- **relationships**:
  - `Profile`: A one-to-one relationship with a `Profile`.
  - `Review`: A user can leave many reviews for sites.
  - `Activity`: A user can participate in many activities through `UserActivity`.

### Profile

The `Profile` model stores additional user information such as:

- **first_name**, **last_name**: Both required and must be alphabetic.
- **email**: Must be unique and valid.

### Review

The `Review` model represents feedback left by users for specific sites. Fields include:

- **description**: Text feedback provided by the user.
- **rating**: A numeric rating between 1 and 10.

### Activity

The `Activity` model represents an activity available at a site. Users can participate in activities, which are logged through the `UserActivity` model.

### Site

The `Site` model represents a location that users can review and participate in activities. Fields include:

- **name**: The name of the site.
- **category**: A category (e.g., nature, cultural, adventure).
- **location**: A foreign key to the `Location` model.

### Location

The `Location` model represents a physical location associated with a site.

## API Endpoints

### Authentication

- **POST /login**  
  Log in a user with their username and password.
  
- **POST /signup**  
  Create a new user account.

- **GET /check_session**  
  Check if the user is currently logged in.

- **DELETE /logout**  
  Log out the current user.

### Users

- **GET /users**  
  Retrieve a list of all users.

- **GET /users/:user_id**  
  Retrieve a specific user by their ID.

### Profiles

- **GET /profiles/:user_id**  
  Retrieve the profile associated with a specific user.

### Reviews

- **GET /reviews**  
  Retrieve a list of all reviews.

- **POST /reviews**  
  Create a new review for a site.

- **GET /reviews/:id**  
  Retrieve a specific review by ID.

### Activities

- **GET /activities**  
  Retrieve a list of all activities.

- **POST /activities**  
  Create a new activity.

- **GET /activities/:id**  
  Retrieve details about a specific activity.

### Sites

- **GET /sites**  
  Retrieve a list of all sites.

- **POST /sites**  
  Create a new site.

- **GET /sites/:id**  
  Retrieve details about a specific site.

### Locations

- **GET /locations**  
  Retrieve a list of all locations.

- **POST /locations**  
  Create a new location.

- **GET /locations/:id**  
  Retrieve details about a specific location.

## Database Setup

The project uses PostgreSQL as the database backend. The connection URI can be set through the `DB_URI` environment variable.

### Creating and Migrating the Database

After setting up the environment and configuring your database, you can run the following commands to create and migrate your database schema:

```bash
flask db init
flask db migrate
flask db upgrade
```

## Seeding Data

To populate the database with some initial data for development purposes, you can use the provided `seed.py` script.

```bash
python seed.py
```

This will generate a set of users, sites, activities, and reviews with random data for testing.

