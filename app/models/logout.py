from datetime import datetime
from . import db


class Logout(db.Model):
    __table_name__ = "logout"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(512), unique=True, nullable=False)
    logout_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, token: str):
        self.token = token
        self.logout_at = datetime.utcnow()

    def __str__(self) -> str:
        return f"<token: {self.token}"

    @staticmethod
    def check_logout(token: str) -> bool:
        # check whether token has been log-out
        token = Logout.query.get(token)
        if token:
            return True
        else:
            return False
