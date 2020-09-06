from datetime import datetime
from marshmallow import fields, Schema
from . import db
from .articles import ArticleSchema

import uuid


class Board(db.Model):
    __table_name__ = "board"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    latest_article = db.Column(db.ARRAY(db.String))
    latest_article_idx = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    articles = db.relationship('Article', backref='board', lazy=True)

    def __init__(self, name: str, user_id: int):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.latest_article_idx = -1
        self.user_id = user_id
        self.created_at = datetime.utcnow()

    def __str__(self) -> str:
        return f"<board: {self.name}, uuid: {self.uuid}"

    def save(self) -> str:
        db.session.add(self)
        db.session.commit()
        return self.uuid

    def update(self, new_name: str) -> str:
        if self.name != new_name:
            setattr(self, 'name', new_name)
        db.session.commit()
        return self.uuid

    def update_latest_article(self, article_uuid: str):
        self.latest_article_idx += 1
        self.latest_article[self.latest_article_idx] = article_uuid
        setattr(self, 'latest_article_idx', self.latest_article_idx)
        setattr(self, 'latest_article', self.latest_article)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_boards():
        return Board.query.all()

    @staticmethod
    def get_boards_by_user(user_id: str):
        return Board.query.filter_by(user_id=user_id).all()

    @staticmethod
    def find_board_by_id(board_id: str):
        return Board.query.get(board_id)

    @staticmethod
    def find_board_by_uuid(board_uuid: str):
        return Board.query.filter_by(uuid=board_uuid).first()

    @staticmethod
    def find_board_by_name(board_name: str):
        return Board.query.filter_by(name=board_name).first()


class BoardSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    latest_article = fields.List(fields.Str())
    latest_article_idx = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    articles = fields.Nested(ArticleSchema, many=True)
