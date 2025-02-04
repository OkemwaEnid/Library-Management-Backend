from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from models import db, User, Book  # Import models
from schemas import UserSchema, BookSchema  # Import schemas
from flask_migrate import Migrate

load_dotenv()  # Load environment variables from .env

# Init app
app = Flask(__name__)
# CORS=(app)
CORS(
    app,
    resources={r"/api/*": {"origins": "https://lms-frontend-ochre-eta.vercel.app/"}},  # Allow React frontend
    supports_credentials=True,  # Allow cookies
)  # Enable CORS for frontend



# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Create a user (Registration)
@app.route('/users', methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    role = request.json.get('role', 'user')  # default role is 'user'

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    # Check if email already exists
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"message": "Email already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    new_user = User(username=username, email=email, password=hashed_password, role=role)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_schema.dump(new_user)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding user", "error": str(e)}), 400


# Login user (Authentication)
@app.route('/login', methods=['POST'])
def login_user():
    email = request.json['email']
    password = request.json['password']

    # Check if email exists in the database
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    # Check if the password is correct
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password"}), 401

    # Login successful
    return jsonify({
        "message": "Login successful",
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }), 200

# Create a book
@app.route('/books', methods=['POST'])
def add_book():
    title = request.json['title']
    author = request.json['author']
    description = request.json['description']

    new_book = Book(title=title, author=author, description=description)

    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify(book_schema.dump(new_book)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding book", "error": str(e)}), 400

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify(books_schema.dump(books))

# Update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    username = request.json.get('username', user.username)
    email = request.json.get('email', user.email)
    password = request.json.get('password', user.password)
    role = request.json.get('role', user.role)

    # Check if username or email already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user and existing_user.id != id:
        return jsonify({"message": "Username already exists"}), 400

    existing_email = User.query.filter_by(email=email).first()
    if existing_email and existing_email.id != id:
        return jsonify({"message": "Email already exists"}), 400

    user.username = username
    user.email = email
    user.password = password
    user.role = role

    try:
        db.session.commit()
        return jsonify(user_schema.dump(user))
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating user", "error": str(e)}), 400

# Update a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    title = request.json.get('title', book.title)
    author = request.json.get('author', book.author)
    description = request.json.get('description', book.description)

    book.title = title
    book.author = author
    book.description = description

    try:
        db.session.commit()
        return jsonify(book_schema.dump(book))
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating book", "error": str(e)}), 400

# Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting user", "error": str(e)}), 400

# Delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting book", "error": str(e)}), 400

# Run server
if __name__ == '__main__':
    app.run(debug=True)
