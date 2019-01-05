import os

from flask import Flask, session, render_template, request, redirect, session, url_for, flash, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
import hashlib
import json
import requests
import time

app = Flask(__name__)
postgresURI = "postgres://bcvcpzwscndkyy:aec11e38db3ab3376ccadd2d83e3e308f60b542e633b44caea6ab7b1a4b422a4@ec2-54-235-169-191.compute-1.amazonaws.com:5432/d3n2ea3ie9begk"
postgresPASS = "aec11e38db3ab3376ccadd2d83e3e308f60b542e633b44caea6ab7b1a4b422a4"
postgresUSER = "bcvcpzwscndkyy"
postgresDB = "d3n2ea3ie9begk"
postgresPORT = 5432
GoodReadsAPIParams = {"key":"vB3wSykxHaLhrIAg5GWZow"}
GoodReadsAPIsecret = "hemIyGOsaG3dpuEBsOcLItY67AL6lsJB9GmRc3dRtg"

# Check for environment variable
os.environ['DATABASE_URL'] = postgresURI
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route("/")
def index():
    session["page"] = "home"
    return render_template("index.html",session=session)


@app.route("/search", methods=["POST", "GET"])
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
                books = db.execute(f"SELECT * FROM books where isbn like '%{isbn}%' and author like '%{author}%' and title like '%{title}%'").fetchall()
                if books:
                    return render_template("search.html", session=session, searchResults = books)
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
    try:
        book = db.execute(f"SELECT * FROM books WHERE isbn = '{book_isbn}';").fetchone()

        if book is None:
            redirect(url_for('search'))
        else:
            if request.method == "POST":
                try:
                    created_on = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    commnet = request.form.get("comment")
                    userrating = request.form.get("starRating")
                    db.execute(f"INSERT INTO bookreviews (username,isbn,comment,stars,created_on) values ('{username}','{book_isbn}','{commnet}','{userrating}',TIMESTAMP '{created_on}');")
                except Exception:
                    flash("Cannot add your comment, you have already reviewed it!")
                finally:
                    db.commit()
    except:
        return render_template("search.html", errormessage=
                               "No result found for your query")

    comments = db.execute("SELECT * FROM bookreviews WHERE isbn = :isbn;",{"isbn":book_isbn}).fetchall()


    goodReadsData = None
    goodReads_reviewcount = None
    goodReads_ratings = None
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
        existsStatus = db.execute(f"SELECT * from account where username='{username}' AND password='{password}'").rowcount != 0
        if existsStatus:
            session['logged_in'] = True
            session['username'] = username
            flash('You were logged in')
            db.execute("UPDATE account SET last_login=TIMESTAMP :vartime WHERE username=:username",{"vartime":str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),"username":username} )
            db.commit()
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
        email = request.form.get("email")
        password = request.form.get("password")
        password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        created_on = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        existsStatus = db.execute(f"SELECT * from account where username='{username}' OR email='{email}'").rowcount != 0
        if existsStatus:
            return render_template("register.html",errormessage=" Username or email are already taken ")
        else:
            db.execute(f"INSERT INTO account (username,email,password,created_on) values('{username}', '{email}','{password}',TIMESTAMP '{created_on}')")
            db.commit()
            flash(" You registered successfully! ")
            session['username'] = username
            return redirect(url_for("login"))

@app.route("/api")
def shortText():
    return "Add ISBN to /api"

@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):

    session["page"] = "api"
    book = db.execute("SELECT * FROM books WHERE isbn='{}'".format(isbn)).fetchone()
    if book is None:
        message = {'status': 404,'message': '%s not found in database'%isbn}
        resp = jsonify(message)
        resp.status_code = 404
        return resp

    else:

        res = {"isbn": isbn, "publication_year": book.year, "author": book.author, "title": book.title }

        GoodReadsAPIParams["isbns"] = isbn
        goodReadsDataRaw = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params=GoodReadsAPIParams)
        goodReads = None
        if goodReadsDataRaw.status_code == 200:
            goodReads = {}
            goodReadsData = goodReadsDataRaw.json()['books'][0]
            goodReads["reviewcount"] = goodReadsData["reviews_count"]
            goodReads["ratings"] = goodReadsData["average_rating"]
            res["review_count"] = goodReads["reviewcount"]
            res["average_score"] = goodReads["ratings"]

        return jsonify(res)




@app.route('/logout')
def logout():
    session["page"] = "logout"
    session.pop('username', None)
    session["logged_in"] = False
    flash('You were logged out')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0')
