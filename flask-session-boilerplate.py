# NOT MINE, This is an example from when I took CS50
# https://cs50.harvard.edu/college/2020/fall/notes/9/

from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

## Uncomment for autorefresh to work with Pixels128/Toolkit/refresh.js
# import uuid
# state = str(uuid.uuid4())
# @app.route("/update")
# def update():
#     return {"state": state}


app.run(host='0.0.0.0', port=80)
