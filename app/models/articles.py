from datetime import datetime
from marshmallow import fields, Schema
from . import db

import uuid


class Article(db.Model):
    __table_name__ = "article"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(128), unique=True, nullable=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, title: str, content: str, board_id: int, user_id: int):
        self.uuid = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.board_id = board_id
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<article: {self.title}, uuid: {self.uuid}"

    def save(self) -> str:
        db.session.add(self)
        db.session.commit()
        return self.uuid

    def update(self, new_title: str, new_content: str):
        if self.title != new_title:
            setattr(self, 'title', new_title)
        if self.content != new_content:
            setattr(self, 'content', new_content)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self.uuid

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_articles_by_user(user_id: str):
        return Article.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_articles_by_board(board_id: str):
        return Article.query.filter_by(board_id=board_id).all()

    @staticmethod
    def get_recent_articles_by_board(board_id: str, article_num: int):
        return Article.query.filter_by(board_id=board_id).order_by(Article.updated_at.desc()).limit(article_num).all()

    @staticmethod
    def find_article_by_id(article_id: str):
        return Article.query.get(article_id)

    @staticmethod
    def find_article_by_uuid(article_uuid: str):
        return Article.query.filter_by(uuid=article_uuid).first()


class ArticleSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.Str(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    board_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(dump_only=True)
