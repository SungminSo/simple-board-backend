from datetime import datetime
from marshmallow import fields, Schema
from . import db, bcrypt
from .boards import BoardSchema
from .articles import ArticleSchema

import uuid


class User(db.Model):
    __table_name__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    boards = db.relationship('boards', backref='user', lazy=True)
    articles = db.relationship('articles', backref='user', lazy=True)

    def __init__(self, email: str, username: str, password: str, is_admin: bool):
        self.uuid = str(uuid.uuid4())
        self.email = email
        self.name = username
        self.password = bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')
        self.is_admin = is_admin
        self.created_at = datetime.utcnow()

    def __str__(self) -> str:
        return f"<user: {self.email}, uuid: {self.uuid}"

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def save(self) -> str:
        db.session.add(self)
        db.session.commit()
        return self.uuid

    def update(self, new_email, new_username, new_password) -> str:
        if self.email != new_email:
            setattr(self, 'email', new_email)
        if self.name != new_username:
            setattr(self, 'name', new_username)
        if self.password != new_password:
            hashed_password = bcrypt.generate_password_hash(new_password, rounds=10).decode('utf-8')
            setattr(self, 'password', hashed_password)
        db.session.commit()
        return self.uuid

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_user_by_id(user_id: str):
        return User.query.get(user_id)

    @staticmethod
    def find_user_by_uuid(user_uuid: str):
        return User.query.get(user_uuid)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.Str(required=True)
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True)
    is_admin = fields.Bool(required=True)
    created_at = fields.DateTime(required=True)
    boards = fields.Nested(BoardSchema, many=True)
    articles = fields.Nested(ArticleSchema, many=True)
