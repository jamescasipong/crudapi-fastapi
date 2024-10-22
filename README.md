Simple CRUD with FastAPI & MongoDB.

# FastAPI User Management API

A simple user management API built with FastAPI, featuring user registration, authentication, and CRUD operations.

## Features

- User registration
- JWT authentication
- Password hashing with bcrypt
- Admin role for user management
- MongoDB integration

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jamescasipong/crudapi-fastapi
   cd crudapi-fastapi
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install fastapi[all] pymongo python-jose passlib
   ```
4. Create .env file and copy and paste the following into the file:
   ```bash
   SECRET_KEY=any_key
   ALGORITHM = HS256
   MONGODB_URL = mongodb://localhost:27017/
   ```
4. Set up your MongoDB database.

## Usage

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
   or
   ```bash
   cd app -> python main.py
   ```

2. Access the API at `http://127.0.0.1:8000/docs`.

3. Use the following endpoints:

### Authentication

- **Login**  
  `POST /token`  
  Request: 
  ```json
  {
      "username": "your_username",
      "password": "your_password"
  }
  ```

- **Register**  
  `POST /register`  
  Request: 
  ```json
  {
      "username": "new_username",
      "password": "new_password",
      "email": "user@example.com"
  }
  ```

### User Management (Protected)

- **Get All Users**  
  `GET /` (Requires JWT)

- **Get User by ID**  
  `GET /{user_id}` (Requires JWT)

- **Create User**  
  `POST /` (Requires JWT and Admin role)

- **Update User**  
  `PUT /{user_id}` (Requires JWT and Admin role)

- **Delete User**  
  `DELETE /{user_id}` (Requires JWT and Admin role)

