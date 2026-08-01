"""REST endpoints for student CRUD and operational health checks."""

import logging
from flask import Blueprint, jsonify, request
from app.db import connect, init_db, serialize

api = Blueprint("api", __name__)
logger = logging.getLogger(__name__)


def valid_payload(payload):
    if not isinstance(payload, dict) or not payload.get("name") or payload.get("age") is None or payload.get("marks") is None:
        return False
    return True


@api.get("/health")
def health():
    try:
        init_db()
        return jsonify(status="healthy"), 200
    except Exception:
        logger.exception("Health check failed")
        return jsonify(status="unhealthy"), 503


@api.get("/students")
def list_students():
    with connect() as db:
        rows = db.execute("SELECT * FROM students ORDER BY id").fetchall()
    return jsonify([serialize(row) for row in rows])


@api.post("/students")
def create_student():
    payload = request.get_json(silent=True)
    if not valid_payload(payload):
        return jsonify(error="name, age, and marks are required"), 400
    with connect() as db:
        cursor = db.execute("INSERT INTO students (name, age, gender, marks) VALUES (?, ?, ?, ?)", (payload["name"], payload["age"], payload.get("gender"), payload["marks"]))
        db.commit()
        student = db.execute("SELECT * FROM students WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(serialize(student)), 201


@api.get("/students/<int:student_id>")
def get_student(student_id):
    with connect() as db:
        student = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    return (jsonify(serialize(student)), 200) if student else (jsonify(error="student not found"), 404)


@api.put("/students/<int:student_id>")
def update_student(student_id):
    payload = request.get_json(silent=True)
    if not valid_payload(payload):
        return jsonify(error="name, age, and marks are required"), 400
    with connect() as db:
        result = db.execute("UPDATE students SET name=?, age=?, gender=?, marks=? WHERE id=?", (payload["name"], payload["age"], payload.get("gender"), payload["marks"], student_id))
        db.commit()
        student = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    return (jsonify(serialize(student)), 200) if result.rowcount else (jsonify(error="student not found"), 404)


@api.delete("/students/<int:student_id>")
def delete_student(student_id):
    with connect() as db:
        result = db.execute("DELETE FROM students WHERE id = ?", (student_id,))
        db.commit()
    return ("", 204) if result.rowcount else (jsonify(error="student not found"), 404)
