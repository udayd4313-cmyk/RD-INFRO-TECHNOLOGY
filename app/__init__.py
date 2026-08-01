"""Application factory and extension setup."""

import logging
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

from app.config import Config
from app.db import init_db
from app.routes import api


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    logging.basicConfig(level=app.config["LOG_LEVEL"], format="%(asctime)s %(levelname)s %(name)s %(message)s")
    app.register_blueprint(api, url_prefix="/api/v1")
    PrometheusMetrics(app, path="/metrics")
    with app.app_context():
        init_db()
    return app
