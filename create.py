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
from model import *

app = Flask(__name__)
postgresURI = "postgres://bcvcpzwscndkyy:aec11e38db3ab3376ccadd2d83e3e308f60b542e633b44caea6ab7b1a4b422a4@ec2-54-235-169-191.compute-1.amazonaws.com:5432/d3n2ea3ie9begk"
# Check for environment variable
os.environ['DATABASE_URL'] = postgresURI
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
def main():
    db.create_all()



if __name__ == '__main__':
    with app.app_context():
        main()
