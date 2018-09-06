import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    headline = "Welcome to Bookhunt! :)"
    today = date.today().strftime("%b %d, %Y")
    weekday = date.today().weekday()
    weekend = weekday == 5 or weekday == 6
    return render_template("index.html", headline=headline, today=today, weekend=weekend)

@app.route("/names", methods=["GET", "POST"])
def names():
    if session.get("names") is None:
        session["names"] = []
    if request.method == "POST":
        name = request.form.get("name")
        session["names"].append(name)

    return render_template("names.html", names=session["names"])

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello.html", name=name)

@app.route("/flights", methods=["GET"])
def flights():
    flights = db.execute("SELECT origin, destination, duration FROM flights").fetchall()
    return render_template("flights.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""

@app.route("/bye")
def bye():
    headline = "Goodbye!"
    return render_template("index.html", headline=headline)

# Comments
# @app.route("/<string:name>")
# def hello(name):
#     name = name.capitalize()
#     return f"<h1>Hello, {name}!</h1>"
