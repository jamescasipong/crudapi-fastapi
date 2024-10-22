Here's a comprehensive README template for your FastAPI project:

```markdown
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
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
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

4. Set up your MongoDB database.

## Usage

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API at `http://127.0.0.1:8000`.

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

## Security

- Use a secure `SECRET_KEY` in your application.
- Configure proper role-based access controls.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgments

Thanks to FastAPI and its community for creating an excellent framework!
```

Feel free to adjust any sections as needed!
