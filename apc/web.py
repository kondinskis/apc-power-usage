from flask import Flask, jsonify, render_template, g, request

from .db import Session, APCReading
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    @app.before_request
    def before_request():
        if "/static/" not in request.path:
            g.session = Session()

    @app.teardown_request
    def teardown_request(exception):
        if "/static/" not in request.path:
            g.session.close()

    @app.get("/")
    def index():
        readings = g.session.query(APCReading).all()
        readings_combined = "Date,Load\\n"
        for reading in readings:
            readings_combined = readings_combined + "{},{}\\n".format(
                reading.date, round(reading.load / reading.no_logs)
            )
        return render_template("index.html", readings=readings_combined)

    return app
