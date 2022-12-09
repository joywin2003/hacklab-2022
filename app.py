from datetime import datetime
from csv import DictReader, DictWriter
from flask import Flask, render_template, session, url_for, request, redirect


db = open("static/users.csv", 'a')
reader = DictReader(db)
writer = DictWriter(db, fieldnames=["username","name","email","password"])


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "q7vytnycnv3y7nc87y8wedssw4ytv5beyv748sytvn74vynt"


title = "scrap dealings"


def isValid(username, password):
    with open("static/users.csv", 'a') as db:
        reader = DictReader(db)
        for row in reader:
            if username == row["username"]:
                if password == row["password"]:
                    return True
    return False


def addUser(username, email, password):
    with open("static/users.csv", 'a') as db:
        writer = DictWriter(db)
        writer.writerow({"username": username, "email": email, "password": password})


@app.route("/")
@app.route("/home")
def index():

    if not session.get("username"):
        return redirect("/login")

    return render_template("index.html", title=title)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if isValid(username, password):
            session["username"] = username
            return redirect('/', title=title)
        
        return render_template("login.html", error="Invalid Password")

    if request.method == "GET":
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.forms.get("username")
        email = request.forms.get("email")
        password = request.forms.get("password")
        # conf_pass = request.forms.get("conf_pass")
        addUser(username, email, password)
        session["username"] = username
        return redirect('/', title=title)

    if request.method == "GET":
        return render_template("register.html")


@app.route("/logout")
def logout():
    session["username"] = None
    redirect("/", title=title)


if __name__ == "__main__":
    app.run(debug=True)