from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import csv

csvFileName = "books.csv"
postgresURI = "postgres://bcvcpzwscndkyy:aec11e38db3ab3376ccadd2d83e3e308f60b542e633b44caea6ab7b1a4b422a4@ec2-54-235-169-191.compute-1.amazonaws.com:5432/d3n2ea3ie9begk"


os.environ['DATABASE_URL'] = postgresURI
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
with open(csvFileName) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    db.execute("START TRANSACTION")
    reader.__next__() # get rid of the first row that doesn't contain useful info
    for isbn, title, author, year in reader:

        db.execute("INSERT INTO books (isbn, title, author, year) values(:isbn, :title, :author, :year)",{"isbn":isbn, "title":title, "author":author, "year":int(year)})
        print("Record %s succesfully inserted!" %isbn)
    db.execute("COMMIT")
    print("All Records uploaded succesfully")
db.commit
