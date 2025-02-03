from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

# User Model (explicitly referring to the 'users' table)
class User(db.Model):  # <-- Here, add the colon at the end of the line
    __tablename__ = 'users'  # Explicitly set table name to 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

# Book Model (explicitly referring to the 'books' table)
class Book(db.Model):
    __tablename__ = 'books'  # Explicitly set table name to 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
