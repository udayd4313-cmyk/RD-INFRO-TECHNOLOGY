"""Small SQLite repository; the database path is configurable for containers."""

import os
import sqlite3
from flask import current_app


def connect():
    database_path = current_app.config["DATABASE_PATH"]
    os.makedirs(os.path.dirname(database_path) or ".", exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect() as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER NOT NULL, gender TEXT, marks REAL NOT NULL)")
        connection.commit()


def serialize(row):
    return dict(row) if row else None
