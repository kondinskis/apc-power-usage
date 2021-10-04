from flask import Flask, jsonify, render_template, g, request

from sqlalchemy import func, text

from .db import Session, APCReading
from .config import Config

freq_opts = {
    "hourly": "%Y-%m-%d %H:00:00.000000",
    "daily": "%Y-%m-%d 00:00:00.000000",
    "monthly": "%Y-%m-01 00:00:00.000000",
}


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
        freq = request.args.get("freq", "hourly")

        statement = text(
            "SELECT id, STRFTIME('{0}', date) as date, AVG(load / no_logs) as load FROM apc_reading GROUP BY STRFTIME('{0}', date)".format(
                freq_opts.get(freq) or freq_opts["hourly"]
            )
        )
        readings = g.session.query(APCReading).from_statement(statement).all()
        readings_combined = "Date,Load\\n"
        for reading in readings:
            readings_combined = readings_combined + "{},{}\\n".format(
                reading.date,
                round(reading.load),
            )
        return render_template("index.html", readings=readings_combined)

    return app
