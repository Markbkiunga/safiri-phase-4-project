# Safiri Project - Backend

## Overview

The Safiri Project backend is designed to manage user authentication, handle data storage, and provide a robust API for the Safiri travel application. This application allows users to create accounts, sign in, and interact with various features of the Safiri platform.

## Features

- **User Authentication**: Secure sign-up and login functionalities.
- **RESTful API**: Provides endpoints for user management and additional features.
- **Data Validation**: Ensures integrity of user inputs.
- **Error Handling**: Comprehensive error messages for improved user experience.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework for Python.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) system for Python.
- **Python**: The programming language used for backend development.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/safiri-project-backend.git
   cd safiri-project-backend


###  Creating a virtual environment
- python -m venv venv
- source venv/bin/activate


### Install dependecies
- pip install -r requirements.txt

## Setting up the database
- Create a database named safiri_db.
- Update the database connection string in your application’s configuration file.


### Running the migrations
- flask db upgrade
- flask db run


## Creating Environment Variables
- Create a .env file in the root directory and set the following environment variables:
## DATABASE_URL=postgresql://username:password@localhost/safiri_db
## SECRET_KEY=your_secret_key


## API Endpoints
- POST /signup

- Creates a new user account.
- Request Body: { "username": "string",      "password": "string" }
- Response:
- 201 Created: User account created successfully.
400 Bad Request: Validation errors.
POST /login

## Additional Endpoints
(You can add other endpoints as your project evolves.)

## Testing
- To run tests for the backend, ensure you have set up your test database. Use the following command:
**pytest

### License
- This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- Flask Documentation
- SQLAlchemy Documentation





