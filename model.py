from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class account(db.Model):
    __tablename__ = 'account'
    username = db.Column(db.String, primary_key = True)
    password = db.Column(db.String,  nullable=False)
    #created_on = db.Column(db.DateTime, nullable=False)
    #last_login= db.Column(db.DateTime, nullable=True)


class books(db.Model):
    __tablename__ = 'books'
    isbn = db.Column(db.String, primary_key = True)
    title = db.Column(db.String,  nullable=False)
    author = db.Column(db.DateTime, nullable=False)
    year= db.Column(db.Integer, nullable=False)



class bookreviews(db.Model):
    __tablename__ = 'bookreviews'
    username = db.Column(db.String, db.ForeignKey("account.username"), nullable = False)
    isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable = False)
    comment = db.Column(db.String, nullable = True)
    stars = db.Column(db.Integer, nullable = False)
    created_on = db.Column(db.DateTime, nullable = True)
    db.PrimaryKeyConstraint(isbn,username)
