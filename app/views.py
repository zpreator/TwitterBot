# app/views.py

from app import app
from flask import render_template


@app.route("/")
def index():

    app.logger.debug(app.config.get("ENV"))

    return render_template("index.html")