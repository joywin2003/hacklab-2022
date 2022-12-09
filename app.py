from datetime import datetime
from csv import DictReader, DictWriter, QUOTE_NONNUMERIC
from flask import Flask, render_template, session, url_for, request, redirect


db = open("static/users.csv", 'a')
reader = DictReader(db)
writer = DictWriter(db, fieldnames=["username","name","email","password"])


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "q7vytnycnv3y7nc87y8wedssw4ytv5beyv748sytvn74vynt"


title = "scrap dealings"

posts = [
    {
        "title": "Title 1",
        "author": "Vyasa",
        "img_src": "https://images.pexels.com/photos/276267/pexels-photo-276267.jpeg?auto=compress&cs=tinysrgb&w=600",
        "time_created": "02:46 AM"
    },
    {
        "title": "Title 2",
        "author": "Samwin",
        "img_src": "https://images.pexels.com/photos/276267/pexels-photo-276267.jpeg?auto=compress&cs=tinysrgb&w=600",
        "time_created": "03:07 AM"
    }
]


def checkCookie(u_name):
    with open("static/user.csv", 'r') as db:
        reader = DictReader(db)
        for row in reader:
            if u_name == row["username"]:
                return True
    return False



def is_logged_in(u_name, p_word):
    with open("static/user.csv", 'r') as db:
        reader = DictReader(db)
        for row in reader:
            if u_name == row["username"] and p_word == row["password"]:
                return True
    return False


def addUser(u_name, e_mail, p_word):
    with open("static/user.csv", 'a') as db:
        writer = DictWriter(db, fieldnames=["username", "email", "password"])
        writer.writerow({"username": u_name, "email": e_mail, "password": p_word}, QUOTE_NONNUMERIC)


@app.route("/")
@app.route("/home")
def index():

    if not session.get("username"):
        return redirect("/login")

    return render_template("index.html", title=title, user=session.get("username"), posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # LOGIN INFO HERE
        username = request.form.get("username")
        password = request.form.get("password")
        if is_logged_in(username, password):
            session["username"] = username
            return redirect('/')
        
        return render_template("login.html", error="Invalid Password")

    if request.method == "GET":
        if checkCookie(session.get("username")):
            return redirect('/')
        else:
            return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # REGISTRATION INFO HERE
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # conf_pass = request.forms.get("conf_pass")
        addUser(username, email, password)
        session["username"] = username
        return render_template("index.html", title=title, user=username)

    if request.method == "GET":
        if checkCookie(session.get("username")):
            return redirect('/')
        else:
            return render_template("register.html")


@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "GET":
        return render_template("post.html")
    if request.method == "POST":
        ...


@app.route("/post/<pid>")
def post_page(pid):
    post_title = ...
    post_author = ...
    img_src = ...
    description = ...

    return render_template("postpage.html", post_title=post_title, post_author=post_author, img_src=img_src, description=description)

    
@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)