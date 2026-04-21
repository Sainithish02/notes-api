# Flask User Management REST API

A backend REST API built using Flask and SQLite that supports full CRUD operations for managing users.

Features

Create users (POST /users)  
Retrieve all users (GET /users)  
Retrieve a specific user (GET /users/<id>)  
Update user details (PUT /users/<id>)  
Delete a user (DELETE /users/<id>)  

Tech Stack

Python  
Flask  
SQLite  
REST API  
JSON  

Project Structure

app.py – Main Flask application  
database.py – Database connection  
models/ – Database query logic  
routes/ – API route definitions  
requirements.txt – Project dependencies  

Example API Request

Create User

POST /users

Request Body

{ "username": "john", "email": "john@example.com" }

Response

{ "message": "user created" }

How to Run the Project

Clone the repository

git clone https://github.com/Sainithish02/flask-user-management-api.git

Go to the project folder

cd flask-user-management-api

Install dependencies

pip install -r requirements.txt

Run the server

python app.py

Server runs at

http://127.0.0.1:5001

Author

Tadi Sai Nithish Reddy  
GitHub: https://github.com/Sainithish02/flask-user-management-api