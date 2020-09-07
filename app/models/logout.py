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

    def __repr__(self) -> str:
        return f"<token: {self.token}"

    def save(self) -> datetime:
        db.session.add(self)
        db.session.commit()
        return self.logout_at

    @staticmethod
    def check_logout(token: str) -> bool:
        # check whether token has been log-out
        token = Logout.query.filter_by(token=token).first()
        if token:
            return True
        else:
            return False
