from flask_sqlalchemy import SQLAlcehemy

db= SQLAlcehemy()

class bookreviews(db.Model):
    username = db.Column(db.String, ForeignKey("account.username"), nullable = False)
    isbn = db.Column(db.String, ForeignKey("books.isbn"), nullable = False)
    comment = db.Column(db.String, nullable = True)
    stars = db.Column(db.Integer, nullable = False)
    created_on = db.Column(db.Date, nullable = True)
    db.UniqueConstraint('username', 'isbn', name='user_book')

class account(db.Model):
    username = db.Column(db.String, primary_key = True)
    password = db.Column(db.String,  nullable=False)
    created_on = db.Column(db.Date, nullable=False)
    last_login= db.Column(db.Date, nullable=True)


class books(db.Model):
    isbn = db.Column(db.String, primary_key = True)
    title = db.Column(db.String,  nullable=False)
    author = db.Column(db.Date, nullable=False)
    year= db.Column(db.Integer, nullable=False)



