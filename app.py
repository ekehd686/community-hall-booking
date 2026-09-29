
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "community-hall-demo-key"

halls = [
    {
        "id": 1,
        "name": "Smt. Jayamma Shivalinge Gowda Function Hall",
        "name_kn": "ಶ್ರೀಮತಿ ಜಯಮ್ಮ ಶಿವಲಿಂಗೇ ಗೌಡ ಫಂಕ್ಷನ್ ಹಾಲ್",
        "phone": "09448750790",
        "location": "SH-7, K.R.S.-K.R.Pete Road, KR Pet, Mandya, Karnataka 571426",
        "capacity": 350,
        "facilities": "AC, 3 rooms, bridal room, electricity backup, 30-car parking",
        "status": "Available",
        "hours": "Hours not publicly listed",
        "price": "₹550 per plate",
        "price_type": "Cost per plate",
        "event_pricing": "Published rate is per plate; wedding/event package may vary.",
        "management_notes": "Outside decorators are not allowed. 50% payment on booking and 50% on the event date. Cancellation depends on the situation.",
        "rating": "4.5/5 (public venue listing)",
        "image_url": "https://img.mandap.com/photos/pictures/33015/orginal/profile_pic_2021-11-28_28129.jpg",
        "source_url": "https://www.mandap.com/mysore/smt-jayamma-shivalinge-gowda-function-hall-in-mysore"
    },
    {
        "id": 2,
        "name": "Srimathi Suvarna Ninge Gowda Function Hall",
        "name_kn": "ಶ್ರೀಮತಿ ಸುವರ್ಣ ನಿಂಗೆ ಗೌಡ ಫಂಕ್ಷನ್ ಹಾಲ್",
        "phone": "Not publicly listed",
        "location": "Sravanabelagola Road, Krishnarajpete, Karnataka 571426",
        "capacity": 100,
        "facilities": "1 room, electricity backup, bridal room, 20-car parking",
        "status": "Available",
        "hours": "Hours not publicly listed",
        "price": "₹380 per plate",
        "price_type": "Cost per plate",
        "event_pricing": "Published rate is per plate; custom event packages may vary.",
        "management_notes": "Outside decorators allowed. Outside DJ and outside alcohol are not allowed. 50% payment on booking; cancellation depends on the situation.",
        "rating": "4.5/5 (public venue listing)",
        "image_url": "https://img.mandap.com/photos/pictures/334353/orginal/profile_pic_2025-09-162.webp",
        "source_url": "https://www.mandap.com/mandya/srimathi-suvarna-ninge-gowda-function-hall-in-mandya"
    },
    {
        "id": 3,
        "name": "ICB Residency and Party Hall",
        "name_kn": "ICB ರೆಸಿಡೆನ್ಸಿ ಮತ್ತು ಪಾರ್ಟಿ ಹಾಲ್",
        "phone": "08485956769",
        "location": "Channarayapatna Main Road / Krishnarajpet Rural, Karnataka 571426",
        "capacity": 320,
        "facilities": "AC, 5 rooms, bridal room, electricity backup, 15-car parking",
        "status": "Available",
        "hours": "Hours not publicly listed",
        "price": "₹50,000 per day",
        "price_type": "Time-based rent",
        "event_pricing": "Published day-rental rate; final wedding/party package should be confirmed with the venue.",
        "management_notes": "Outside decorators are not allowed. Outside DJ and outside food are allowed. Outside alcohol is not allowed. 50% payment on booking and 50% on the event date.",
        "rating": "4.5/5 (public venue listing)",
        "image_url": "https://img.mandap.com/photos/pictures/327881/orginal/profile_pic_icb1.png",
        "source_url": "https://www.mandap.com/mandya/icb-residency-and-party-hall-in-mandya"
    },
    {
        "id": 4,
        "name": "Nanjamma Muddegowda Samudaya Bhavana",
        "name_kn": "ನಂಜಮ್ಮ ಮುದ್ದೇಗೌಡ ಸಮುದಾಯ ಭವನ",
        "phone": "Not publicly listed",
        "location": "Main Road, near KR Pete Town Club, Krishnarajpete, Mandya, Karnataka 571426",
        "capacity": 400,
        "facilities": "10 rooms, bridal room, electricity backup, 50-car parking, dining hall",
        "status": "Available",
        "hours": "24 hours (public listing; some days may differ)",
        "price": "₹80,000 per day",
        "price_type": "Time-based rent",
        "event_pricing": "Published day-rental rate; event package and final availability should be confirmed.",
        "management_notes": "Outside decorators are not allowed. Outside food is allowed. 50% payment on booking and 50% on the event date; cancellation depends on the situation.",
        "rating": "4.0/5 on Justdial; 4.5/5 on Mandap/WeddingBazaar",
        "image_url": "https://img.weddingbazaar.com/photos/pictures/006/300/510/new_large/ss20230327-17041-1p025uy.jpg",
        "source_url": "https://www.mandap.com/mandya/nanjamma-muddegowda-samudaya-bhavana-in-mandya"
    },
    {
        "id": 5,
        "name": "Shree Lakshmi Venkateshwara Convention Hall K R Pete",
        "name_kn": "ಶ್ರೀ ಲಕ್ಷ್ಮೀ ವೆಂಕಟೇಶ್ವರ ಕನ್ವೆನ್ಷನ್ ಹಾಲ್",
        "phone": "Not publicly listed",
        "location": "K R Pete, Krishnarajpete, Mandya, Karnataka 571426",
        "capacity": 400,
        "facilities": "Convention hall; public listing shows event-space photos",
        "status": "Available",
        "hours": "Business hours not publicly listed",
        "price": "Contact hall for price",
        "price_type": "Custom package",
        "event_pricing": "No reliable public event price found; request a quote for wedding, birthday or meeting.",
        "management_notes": "No specific management issue or policy was reliably published in the sources checked.",
        "rating": "4.2/5 (123 public ratings)",
        "image_url": "",
        "source_url": "https://www.justdial.com/Mandya/Shree-Lakshmi-Venkateshwara-Convention-Hall-K-R-Pete-Krishnarajapete/9999P8232-8232-240426190049-S8Y8_BZDET"
    }
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
