from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = "account"
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.Timestamp, nullable=False)
    last_login = db.Column(db.Timestamp, nullable=True)


class Book(db.Model):
    __tablename__ = "book"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)


class Bookreviews(db.Model):
    __tablename__ = "bookreviews"
    username = db.Column(db.String, db.ForeignKey("account.username"), nullable=False)
    isbn = db.Column(db.String, db.ForeignKey("book.isbn"), nullable=False)
    comment = db.Column(db.String, nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.Timestamp, nullable=False)
