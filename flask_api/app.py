# app.py
from flask import render_template # Remove: import Flask
import connexion

from django_api.init_django import init
init()

from django_api.api.models import SciRecord

app = connexion.App(__name__, specification_dir="./")

app.add_api("swagger.yml")


@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)