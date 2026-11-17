"""
STUDENT COURSE API
Laboratory Activity 3A - Creating a Backend API

A small, read-only REST API built with Python and Flask.

The API serves six fictional university courses. The course list lives in
this file as plain Python data: there is no database, no login, and no way
to create, update or delete records.

Run locally:     python app.py
Run on Render:   gunicorn app:app
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS

# ---------------------------------------------------------------------------
# 1. Create the Flask application object.
#    The variable name "app" matters: Render starts this project with
#    "gunicorn app:app", which means "import the variable named app from the
#    file app.py".
# ---------------------------------------------------------------------------
app = Flask(__name__)

# ---------------------------------------------------------------------------
# 2. Allow browsers on other origins to read the JSON (CORS).
#    A wide-open policy is acceptable for a classroom demonstration because
#    every route is read-only and contains no personal information.
# ---------------------------------------------------------------------------
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------------------------------------------------------------------------
# 3. Sample data.
#    All six courses below are fictional. Each course is a dictionary with
#    exactly four keys: id (integer), code, name and description.
# ---------------------------------------------------------------------------
COURSES = [
    {
        "id": 1,
        "code": "CS 101",
        "name": "Introduction to Computing",
        "description": "A first look at how computers store and process information, covering number systems, hardware basics and simple algorithms.",
    },
    {
        "id": 2,
        "code": "IT 210",
        "name": "Data Structures and Algorithms",
        "description": "Organizing data with lists, stacks, queues, trees and graphs, then measuring how quickly common algorithms solve problems.",
    },
    {
        "id": 3,
        "code": "IS 220",
        "name": "Systems Integration and Architecture",
        "description": "How separate systems exchange data through APIs, middleware and message queues to form one working enterprise solution.",
    },
    {
        "id": 4,
        "code": "CS 230",
        "name": "Database Management Systems",
        "description": "Designing relational tables, writing SQL queries, and keeping stored data accurate with keys, constraints and normalization.",
    },
    {
        "id": 5,
        "code": "IT 240",
        "name": "Web Systems and Technologies",
        "description": "Building and deploying web applications: HTTP, HTML and CSS, server-side logic, sessions and basic security.",
    },
    {
        "id": 6,
        "code": "CS 250",
        "name": "Software Engineering",
        "description": "Turning requirements into working software using agile planning, version control, automated testing and team code review.",
    },
]


def find_course(course_id):
    """Return the course dictionary with this id, or None when it does not exist."""
    for course in COURSES:
        if course["id"] == course_id:
            return course
    return None


# ---------------------------------------------------------------------------
# 4. Endpoints (routes).
# ---------------------------------------------------------------------------
@app.get("/api/health")
def health_check():
    """Health check: proves the service is online and answering requests."""
    return jsonify({
        "status": "success",
        "message": "Student Course API is running",
    }), 200


@app.get("/api/courses")
def list_courses():
    """Course list: returns every course as a JSON array."""
    return jsonify(COURSES), 200


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    """Single course: returns one course, or HTTP 404 when the id is unknown."""
    course = find_course(course_id)
    if course is None:
        return jsonify({
            "status": "error",
            "message": f"Course with id {course_id} was not found.",
        }), 404
    return jsonify(course), 200


# ---------------------------------------------------------------------------
# 5. Error handling.
#    Every error is answered in JSON, so a client never receives an HTML page
#    it cannot read.
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    """Unknown URL, or a course id that is not a whole number."""
    return jsonify({
        "status": "error",
        "message": "The requested resource was not found.",
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """This API is read-only, so anything other than GET is rejected."""
    return jsonify({
        "status": "error",
        "message": "This API only accepts GET requests.",
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """A safe message instead of a stack trace."""
    return jsonify({
        "status": "error",
        "message": "An unexpected server error occurred.",
    }), 500


# ---------------------------------------------------------------------------
# 6. Local development entry point.
#    Render does not use this block: there, gunicorn imports "app" and serves
#    it. The block runs only when you start the file yourself with
#    "python app.py".
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)