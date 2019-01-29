import os, sys, traceback,time,requests, hashlib
from flask import Flask, session, render_template, request, redirect, session, url_for, flash, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from Models import *

app = Flask(__name__)

postgresURI = "postgres://bcvcpzwscndkyy:aec11e38db3ab3376ccadd2d83e3e308f60b542e633b44caea6ab7b1a4b422a4@ec2-54-235-169-191.compute-1.amazonaws.com:5432/d3n2ea3ie9begk"
postgresPORT = 5432
GoodReadsAPIParams = {"key":"vB3wSykxHaLhrIAg5GWZow"}

# Check for environment variable
os.environ['DATABASE_URL'] = postgresURI
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db.init_app(app)
Session(app)

likeTemplate = '%{}%'

@app.route("/")
def index():
    session["page"] = "home"
    return render_template("index.html", session=session)

@app.route("/search", methods=["GET","POST"])
def search():
    session["page"] = "search"
    if session.get("logged_in", False) is False:
        flash('You need to login to access search page')
        return redirect(url_for("login"))
    else:
        if request.method == "GET":
            return render_template("search.html", session=session)
        else:
            isbn = request.form.get("isbn").replace(" ", "")
            author = request.form.get("author").replace(" ", "")
            title = request.form.get("title").replace(" ", "")

            if author != "" or title != "" or isbn != "":
                booksQuery = Book.query.filter(and_(Book.isbn.like('%{}%'.format(isbn)), Book.author.like('%{}%'.format(author)), Book.title.like('%{}%'.format(title)))).all()
                if booksQuery:
                    return render_template("search.html", session=session, searchResults = booksQuery)
                else:
                    flash("Your query yeilded no results")
                    return render_template("search.html", session=session)
            else:
                flash("No valid query made")
                return render_template("search.html", session=session)



@app.route("/search/<book_isbn>", methods=["POST", "GET"])
def booksearch(book_isbn):

    session["page"] = "search"
    username = session['username']
    if session.get("logged_in", False) is False:
        flash('You need to login to access search page')
        return redirect(url_for("login"))
    book = Book.query.get(book_isbn)
    if book is None:
        redirect(url_for('search'))
    else:
        if request.method == "POST":
            created_on = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            comment = request.form.get("comment")
            userrating = request.form.get("starRating")
            newReview = Bookreview(username=username,isbn=book_isbn,comment=comment,stars=userrating,created_on=created_on)
            succesful = Bookreview.addReview(newReview)
            if not succesful:
                flash("you cannot add more comments, you have already reviewed")

    comments = Bookreview.query.filter_by(isbn = book_isbn).all()
    GoodReadsAPIParams["isbns"] = book_isbn
    goodReadsDataRaw = requests.get("https://www.goodreads.com/book/review_counts.json",
                   params=GoodReadsAPIParams)
    goodReads = None
    if goodReadsDataRaw.status_code == 200:
        goodReads = {}
        goodReadsData = goodReadsDataRaw.json()['books'][0]
        goodReads["reviewcount"] = goodReadsData["reviews_count"]
        goodReads["ratings"] = goodReadsData["average_rating"]

    return render_template("book.html", book=book, comments=comments,goodReads=goodReads )


@app.route("/login", methods=["POST", "GET"])
def login():
    session["page"] = 'login'
    if request.method == "GET":
        return render_template("login.html", session = session)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        existsStatus = Account.query.filter(and_(Account.username==username,  Account.password == password)).first() is not None
        if existsStatus:
            session['logged_in'] = True
            session['username'] = username
            flash('You were logged in')
            user = Account.query.filter_by(username=username).first()
            user.update_last_login()
            db.session.commit()
            return redirect(url_for("search"))
        else:
            return render_template("login.html",session= session,errormessage=" Username or password are incorrect")


@app.route("/register", methods=["POST", "GET"])
def register():
    session["page"] = "register"
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        created_on = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        existsStatus = Account.query.filter_by(
            username = username).first()
        print("existsStatus = %s" %existsStatus )
        if existsStatus:
            return render_template("register.html",errormessage=" Username are already taken ")
        else:
            newUser = Account(username=username, password=password, created_on=created_on)
            db.session.add(newUser)
            db.session.commit()
            flash(" You registered successfully! ")
            session['username'] = username
            return redirect(url_for("login"))

@app.route("/api")
def shortText():
    return "Add ISBN to /api"

@app.route("/api/<isbn>", methods=["GET", "POST","PUT","DELETE"])
def api(isbn):
    session["page"] = "api"
    book = Book.query.get(isbn)

    ErrorMessage = jsonify({'status': 404,'message': '%s not found in database'%isbn})
    ErrorMessage.status_code = 404

    successMessage = jsonify({'status': 200, 'message': 'operation done succesfully'})
    successMessage.status_code = 200

    if book is None:
        return ErrorMessage
    else:
        if request.method == "GET":
            res = {"isbn": isbn, "publication_year": book.year, "author": book.author, "title": book.title }
            GoodReadsAPIParams["isbns"] = isbn
            goodReadsDataRaw = requests.get("https://www.goodreads.com/book/review_counts.json",
						   params=GoodReadsAPIParams)
            if goodReadsDataRaw.status_code == 200:
                goodReads = {}
                goodReadsData = goodReadsDataRaw.json()['books'][0]
                goodReads["reviewcount"] = goodReadsData["reviews_count"]
                goodReads["ratings"] = goodReadsData["average_rating"]
                res["review_count"] = goodReads["reviewcount"]
                res["average_score"] = goodReads["ratings"]
            return jsonify(res)
        elif request.method == "POST":
            data = request.args
            try:
                comment = data.get("comment")
                stars = data.get("stars")
                username = data.get("username")
            except:
                return {'status':500, "message":"cannot exctract post parameters"}
            created_on = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            newReview = Bookreview(username=username, isbn=isbn, comment=comment, stars=stars,
                                   created_on=created_on)
            succesful = Bookreview.addReview(newReview)
            if not succesful:
                ErrorMessage = jsonify({'status': 500,'message': 'Cannot add the comment'})
                ErrorMessage.status_code = 500
                return ErrorMessage
            else:
                return successMessage
        elif request.method == "PUT":
            data = request.args
            try:
                comment = data.get("comment")
                stars = data.get("stars")
                username = data.get("username")
            except:
                return {'status': 500, "message": "cannot exctract post parameters"}
            try:
                print("username=%s"%username)
                book = Bookreview.query.filter(and_(Bookreview.isbn == isbn,Bookreview.username == username)).one()
                if book:
                    book.stars = stars
                    book.comment = comment
                    db.session.commit()
                    return successMessage
                else:
                    ErrorMessage = jsonify({'status': 421, 'message': 'book not found'})
                    ErrorMessage.status_code = 421
                    return ErrorMessage
            except Exception as e:
                ErrorMessage = jsonify({'status': 422 , 'content': str(e)})
                ErrorMessage.status_code = 422
                return ErrorMessage
        elif request.method == "DELETE":
            data = request.args
            try:
                username = data.get("username")
            except:
                return {'status': 500, "message": "cannot exctract post parameters"}
            try:
                review = Bookreview.query.filter(and_(Bookreview.isbn == isbn,Bookreview.username == username)).one()
                if review:
                    try:
                        db.session.delete(review)
                        db.session.commit()
                        return successMessage
                    except Exception as e:
                        ErrorMessage = jsonify({'status': 420, 'content': str(e), 'message':'unable to delete the review'})
                        ErrorMessage.status_code = 420
                        return ErrorMessage

                else:
                    ErrorMessage = jsonify({'status': 301, "message": "book not found"})
                    ErrorMessage.status_code = 301
                    return ErrorMessage

            except Exception as e:
                ErrorMessage = jsonify({'status': 302, 'content': str(e)})
                ErrorMessage.status_code = 302
                return ErrorMessage






@app.route('/logout')
def logout():
    session["page"] = "logout"
    session.pop('username', None)
    session["logged_in"] = False
    flash('You were logged out')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)
