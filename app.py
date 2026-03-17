from flask import Flask, render_template, request, redirect, url_for, flash
from models import ClinicQueue

app = Flask(__name__)
app.secret_key = "clinic_secret_key_2026"

# Global queue instance — lives in memory for the session
queue = ClinicQueue()


@app.route("/")
def index():
    """Home page — shows the current waiting queue and stats."""
    return render_template(
        "index.html",
        waiting_list=queue.get_waiting_list(),
        waiting_count=queue.waiting_count(),
        seen_count=queue.seen_count(),
        can_undo=queue.can_undo(),
        avg_wait=queue.average_wait_time(),
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration page — form to add a new patient to the queue."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        complaint = request.form.get("complaint", "").strip()
        priority = request.form.get("priority", "Normal").strip()
        notes = request.form.get("notes", "").strip()
        gender = request.form.get("gender", "").strip()

        # Basic validation
        if not name or not age or not complaint:
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        try:
            age = int(age)
            if age <= 0 or age > 120:
                raise ValueError
        except ValueError:
            flash("Please enter a valid age (1-120).", "error")
            return redirect(url_for("register"))

        if any(c.isdigit() for c in name):
            flash("Name cannot contain numbers.", "error")
            return redirect(url_for("register"))

        if priority not in ("Normal", "Urgent", "Emergency"):
            priority = "Normal"

        patient = queue.register_patient(name, age, complaint, priority, notes, gender)
        return render_template("register.html", success=True, patient=patient)

    return render_template("register.html")


@app.route("/call-next", methods=["POST"])
def call_next():
    """Calls the next patient from the front of the queue (FIFO)."""
    patient = queue.call_next_patient()
    if patient:
        flash(f"🔔 Now calling: {patient.name} — Ticket #{patient.ticket_number}", "success")
    else:
        flash("⚠️ The waiting queue is empty.", "error")
    return redirect(url_for("index"))


@app.route("/undo", methods=["POST"])
def undo():
    """Restores the last called patient back to the queue."""
    patient = queue.undo_last_call()
    if patient:
        flash(f"↩️ Restored {patient.name} back to the queue.", "success")
    else:
        flash("⚠️ Nothing to undo.", "error")
    return redirect(url_for("index"))


@app.route("/seen-today")
def seen_today():
    """Shows all patients that have been attended to today."""
    return render_template(
        "seen_today.html",
        seen_list=queue.get_seen_today(),
        seen_count=queue.seen_count(),
    )


if __name__ == "__main__":
    app.run(debug=True)
