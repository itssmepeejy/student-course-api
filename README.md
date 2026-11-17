# Student Course API

A small, read-only REST API built with **Python** and **Flask** for
**Laboratory Activity 3A - Creating a Backend API**
(System Integration and Architecture).

The API returns six fictional university courses. All course data lives directly
in `app.py`: there is no database, no login, and no way to create, update or
delete records.

## Project structure

```
student-course-api/
├── app.py
├── requirements.txt
└── README.md
```

| File | What it does |
| --- | --- |
| `app.py` | Creates the Flask application, holds the sample course data and defines the three GET endpoints. |
| `requirements.txt` | Lists the Python packages that pip installs before the app starts. |
| `README.md` | These instructions. |

## Endpoints

| Method | Path | What it returns | Success | Errors |
| --- | --- | --- | --- | --- |
| GET | `/api/health` | A short status message confirming the API is running | `200` | - |
| GET | `/api/courses` | A JSON array containing all six courses | `200` | - |
| GET | `/api/courses/<id>` | The single course that matches the integer `id` | `200` | `404` when no course has that id |

The API is read-only and only answers `GET` requests. Any other method returns `405`.

### Example responses

`GET /api/health`

```json
{
  "status": "success",
  "message": "Student Course API is running"
}
```

`GET /api/courses/1`

```json
{
  "id": 1,
  "code": "CS 101",
  "name": "Introduction to Computing",
  "description": "A first look at how computers store and process information, covering number systems, hardware basics and simple algorithms."
}
```

`GET /api/courses/99` returns HTTP `404`

```json
{
  "status": "error",
  "message": "Course with id 99 was not found."
}
```

## Run it on your computer

You need Python 3.9 or newer.

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Install the dependencies and start the server:

```bash
pip install -r requirements.txt
python app.py
```

The API is now available at `http://127.0.0.1:5000`.

## Test the endpoints

Open these URLs in a browser:

- http://127.0.0.1:5000/api/health
- http://127.0.0.1:5000/api/courses
- http://127.0.0.1:5000/api/courses/1
- http://127.0.0.1:5000/api/courses/99 (should show a 404 error message)

Or with curl:

```bash
curl http://127.0.0.1:5000/api/health
curl http://127.0.0.1:5000/api/courses
curl http://127.0.0.1:5000/api/courses/1
curl -i http://127.0.0.1:5000/api/courses/99
```

## Deploy to Render

1. Upload this folder to a GitHub repository named `student-course-api`.
2. In Render, choose **New -> Web Service** and connect that repository.
3. Use these settings:

| Setting | Value |
| --- | --- |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

`app:app` means "the variable called `app` inside the file `app.py`". Render sets
the `PORT` environment variable automatically and `app.py` reads it, so no extra
configuration is needed.

When the deploy finishes, open `https://your-service.onrender.com/api/health`.

## Notes

- Free Render services go to sleep after a period without traffic, so the first
  request can take up to a minute.
- The course data is sample data written by hand. This project does not connect
  to any database.
- CORS is open for every `/api/` route so a classroom demo page can call the API
  from another origin. Nothing sensitive is exposed because the API is read-only.
