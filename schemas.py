# app/schemas.py

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import User, Book


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

class BookSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Book
