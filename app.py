
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "community-hall-demo-key"

halls = [
    {"id": 1, "name": "Community Hall A", "location": "Main Road", "capacity": 300,
     "facilities": "Stage, chairs, sound system, parking", "status": "Available"},
    {"id": 2, "name": "Community Hall B", "location": "Gandhi Nagar", "capacity": 500,
     "facilities": "Stage, projector, AC, parking", "status": "Available"},
    {"id": 3, "name": "Community Hall C", "location": "Station Road", "capacity": 200,
     "facilities": "Chairs, kitchen, parking", "status": "Available"},
]

bookings = [
    {"id": 1001, "hall_id": 1, "hall": "Community Hall A", "name": "Sample User",
     "phone": "9876543210", "date": "2026-10-15", "start": "10:00",
     "end": "16:00", "purpose": "Community meeting", "status": "Approved"},
]

maintenance = [
    {"id": 1, "hall_id": 3, "hall": "Community Hall C",
     "date": "2026-10-20", "description": "Electrical inspection", "status": "Scheduled"}
]

def is_available(hall_id, date, start, end):
    for m in maintenance:
        if m["hall_id"] == hall_id and m["date"] == date and m["status"] == "Scheduled":
            return False
    for b in bookings:
        if b["hall_id"] != hall_id or b["date"] != date or b["status"] in ("Rejected", "Cancelled"):
            continue
        # Simple time overlap check
        if start < b["end"] and end > b["start"]:
            return False
    return True

@app.route("/")
def index():
    return render_template("index.html", halls=halls, bookings=bookings, maintenance=maintenance)

@app.route("/halls")
def halls_page():
    return render_template("halls.html", halls=halls)

@app.route("/book/<int:hall_id>", methods=["GET", "POST"])
def book(hall_id):
    hall = next((h for h in halls if h["id"] == hall_id), None)
    if not hall:
        return "Hall not found", 404

    if request.method == "POST":
        date = request.form["date"]
        start = request.form["start"]
        end = request.form["end"]

        if start >= end:
            flash("End time must be later than start time.", "error")
            return redirect(url_for("book", hall_id=hall_id))

        if not is_available(hall_id, date, start, end):
            flash("This hall is not available for the selected date and time.", "error")
            return redirect(url_for("book", hall_id=hall_id))

        new_id = max([b["id"] for b in bookings], default=1000) + 1
        bookings.append({
            "id": new_id, "hall_id": hall_id, "hall": hall["name"],
            "name": request.form["name"], "phone": request.form["phone"],
            "date": date, "start": start, "end": end,
            "purpose": request.form["purpose"], "status": "Pending"
        })
        flash(f"Booking request #{new_id} submitted successfully.", "success")
        return redirect(url_for("my_bookings"))

    return render_template("booking.html", hall=hall)

@app.route("/my-bookings")
def my_bookings():
    return render_template("my_bookings.html", bookings=bookings)

@app.route("/admin")
def admin():
    return render_template("admin.html", halls=halls, bookings=bookings, maintenance=maintenance)

@app.route("/admin/booking/<int:booking_id>/<action>")
def booking_action(booking_id, action):
    b = next((x for x in bookings if x["id"] == booking_id), None)
    if b and action in ("approve", "reject", "cancel"):
        b["status"] = {"approve": "Approved", "reject": "Rejected", "cancel": "Cancelled"}[action]
        flash(f"Booking #{booking_id} updated to {b['status']}.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/maintenance", methods=["POST"])
def add_maintenance():
    hall_id = int(request.form["hall_id"])
    hall = next(h for h in halls if h["id"] == hall_id)
    maintenance.append({
        "id": max([m["id"] for m in maintenance], default=0) + 1,
        "hall_id": hall_id, "hall": hall["name"],
        "date": request.form["date"],
        "description": request.form["description"],
        "status": "Scheduled"
    })
    flash("Maintenance schedule added.", "success")
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)
