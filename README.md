# Online Course Assessment

Django application with courses, lessons, questions, multiple-choice exams, submissions, and result evaluation.

## Run on Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
$env:DEMO_PASSWORD = "CourseDemo2026!"
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/onlinecourse/ or http://127.0.0.1:8000/admin/.
Local demo username: `assylkhan`. Password: the value you set in `DEMO_PASSWORD`.
The seed command only sets the password when it creates the account.

## Run on macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
DEMO_PASSWORD='CourseDemo2026!' .venv/bin/python manage.py seed_demo
.venv/bin/python manage.py runserver
```

## Validate

```bash
python manage.py check
python manage.py test
```

Six tests cover successful submission, partial/extra/empty answers, invalid and cross-course choices, result ownership, login, and POST requirements.

## Grading files

| Task | File |
| --- | --- |
| 1 | onlinecourse/models.py |
| 2 | onlinecourse/admin.py |
| 3 | screenshots/03-admin-site.png |
| 4 | onlinecourse/templates/onlinecourse/course_details_bootstrap.html |
| 5 | onlinecourse/views.py |
| 6 | onlinecourse/urls.py |
| 7 | screenshots/07-final.png |

Screenshots show this application running locally with the seeded mock course. The successful attempt is computed by the application after submitting all correct choices. For a question with multiple correct choices, every correct choice must be selected and no incorrect choice may be selected. A score of at least 70% passes.

## GitHub

Create a public repository named `onlinecourse-final-project` with branch `main`, upload the contents of this folder, and use the file links listed in SUBMISSION_RU.md. This project does not include a database or saved credentials.

This configuration is for local development. Set a private DJANGO_SECRET_KEY, set DJANGO_DEBUG=0, configure allowed hosts, and use a production server before deploying publicly.

Screenshot capture: Chromium rendered responses from this Django application through the Django test client, including login, POST submission, database persistence, and result evaluation. No result text or score was drawn or edited into the images.
