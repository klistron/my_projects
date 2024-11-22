from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from webapp.db import db
from webapp.main.models import Order


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    first_name = db.Column(db.String(500), nullable=True)
    middle_name = db.Column(db.String(1000), nullable=True)
    username = db.Column(db.String(1000), nullable=True)
    last_name = db.Column(db.String(1000), nullable=True)
    phone = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(1000), nullable=True)
    password = db.Column(db.String(1000), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=True)

    orders = relationship("Order", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
