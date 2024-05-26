from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class Role:
    Admin = "Admin"
    Manager = "Manager"
    Analyst = "Analyst"


class Group:
    Customer1 = "Customer 1"
    Customer2 = "Customer 2"
    Customer3 = "Customer 3"


class Status:
    Pending = "Pending"
    In_review = "In review"
    Closed = "Closed"


class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255))
    role = db.Column(db.String(64), default=Role.Analyst, nullable=False)
    group = db.Column(db.String(64), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Ticket(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), nullable=False, default=Status.Pending)
    note = db.Column(db.Text, nullable=True)
    user_create = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_work = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Ticket {self.id} {self.status}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))