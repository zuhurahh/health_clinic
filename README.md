# 🏥 ClinicQ — Health Clinic Queue Manager

A Flask web application that manages patient registration and queuing at a health clinic. Built as part of COS 202 Assignment 4 at MAAUN.

---

## What the App Does

- **Register patients** with their name, age, and chief complaint
- **Manage a waiting queue** using a First-In, First-Out (FIFO) data structure — the first patient registered is the first to be called
- **Call the next patient** with a single button click
- **View all patients seen today** with timestamps showing when they registered and when they were attended to
- **Live stats** showing how many patients are waiting and how many have been seen

---

## Project Structure

```
clinic_queue/
│
├── app.py              # Flask routes and application logic
├── models.py           # OOP classes: Patient and ClinicQueue
├── requirements.txt    # Python dependencies
├── README.md           # This file
│
└── templates/
    ├── base.html       # Shared layout (nav, styles, flash messages)
    ├── index.html      # Home page — waiting queue
    ├── register.html   # Register a new patient
    └── seen_today.html # Patients attended to today
```

---

## How to Run the App Locally (Step-by-Step)

Follow these steps exactly. No prior experience needed.

### Step 1 — Make sure Python is installed

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and type:

```bash
python --version
```

You should see something like `Python 3.10.x`. If you get an error, download Python from [python.org](https://python.org).

---

### Step 2 — Download the project

If you have Git installed:

```bash
git clone https://github.com/zuhurahh/health_clinic.git
cd clinic-queue
```

Or just download the ZIP from GitHub and unzip it, then open your terminal inside that folder.
---

### Step 3 — Install Flask

In your terminal, run:

```bash
pip install Flask
```

This downloads and installs Flask (the web framework the app is built on).

---

### Step 4 — Run the app

```bash
python app.py
```

You will see output like:

```
 * Running on http://127.0.0.1:5000
```

---

### Step 5 — Open in your browser

Open your web browser and go to:

```
http://127.0.0.1:5000
```

The app is now running! You can register patients, call the next patient, and view today's records.

To stop the app, press `Ctrl + C` in the terminal.

---

## Technical Concepts Used

| Concept | How It's Used |
|---|---|
| **OOP (Classes)** | `Patient` class with `__init__`, `get_summary()`, `to_dict()` methods. `ClinicQueue` class encapsulates all queue logic. |
| **Data Structure — Queue (FIFO)** | `collections.deque` is used inside `ClinicQueue`. `.append()` adds to the back; `.popleft()` removes from the front — true FIFO behaviour. |
| **Standard API — datetime** | Every `Patient` is timestamped at registration using `datetime.now()`. Seen-at time is also recorded when a patient is called. |
| **Flask Routes** | `GET /` home page, `GET/POST /register`, `POST /call-next`, `GET /seen-today` |
| **Jinja2 Templates** | HTML templates inherit from `base.html` and receive Python data via `render_template()` |

---

## Author

Built by zuhra dangyatin — COS 202, MAAUN, 2026.
