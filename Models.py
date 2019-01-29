from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'
    isbn = db.Column(db.String, primary_key = True)
    title = db.Column(db.String,  nullable=False)
    author = db.Column(db.String, nullable=False)
    year= db.Column(db.Integer, nullable=False)

class Account(db.Model):
    __tablename__ = 'account'
    username = db.Column(db.String, primary_key = True)
    password = db.Column(db.String,  nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    last_login= db.Column(db.DateTime, nullable=True)
    def update_last_login(self):
        self.last_login  = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class Bookreview(db.Model):
    __tablename__ = 'bookreviews'
    username = db.Column(db.String, db.ForeignKey("account.username"), nullable = False)
    isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable = False)
    comment = db.Column(db.String, nullable = False)
    stars = db.Column(db.Integer, nullable = False)
    created_on = db.Column(db.DateTime, nullable = False)
    db.PrimaryKeyConstraint(isbn,username)
    def addReview(newReview):
        try:
             db.session.add(newReview)
             db.session.commit()
             return True
        except:
             db.session().rollback()
             return False
