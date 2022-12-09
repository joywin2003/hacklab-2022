from flask import Flask

app = Flask(__name__)
app.secret_key = "I LIKE GIRLS"

from scrap import routes