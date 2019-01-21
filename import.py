import os
import csv
from models import Book
from flask import Flask, render_template, request
from models import *

csvFileName = "books.csv"
postgresURI = "postgres://bcvcpzwscndkyy:aec11e38db3ab3376ccadd2d83e3e308f60b542e633b44caea6ab7b1a4b422a4@ec2-54-235-169-191.compute-1.amazonaws.com:5432/d3n2ea3ie9begk"

app = Flask(__name__)
os.environ["DATABASE_URL"] = postgresURI
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    with open(csvFileName) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.__next__() # get rid of the first row that doesn't contain useful info
        for isbn, title, author, year in reader:
            #db.execute("INSERT INTO books (isbn, title, author, year) values(:isbn, :title, :author, :year)",{"isbn":isbn, "title":title, "author":author, "year":int(year)})
            newBook = Book(isbn=isbn, title= title, author= author, year= int(year))
            db.session.add(newBook)
        db.session.commit()
        print("Record %s succesfully inserted!" %isbn)
    print("All Records uploaded succesfully")
