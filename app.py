from flask import Flask, render_template, request, redirect, session, flash, url_for
import database as db
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hotel123"


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "GET":
        return render_template("login.html")

    
    role = request.form.get("role")
    
   
    captcha_input = request.form.get("captcha_input", "").strip()
    captcha_answer = request.form.get("captcha_answer", "").strip()
    
    if not captcha_input or (captcha_input != captcha_answer):
        flash("Security Check Failed. Please try the math again.", "danger")
        return render_template("login.html")

    
    if role == "admin":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            flash("Please enter admin username and password.", "danger")
            return render_template("login.html")
            
        if db.validate_admin(username, password):
            session["admin"] = username
            flash("Welcome back, Administrator.", "success")
            return redirect("/admin_dashboard")
        
        flash("Invalid admin credentials.", "danger")
        return render_template("login.html")

    
    else:
        email = request.form.get("email")
        phone = request.form.get("phone")
        
        if not email or not phone:
            flash("Please enter email and phone.", "danger")
            return render_template("login.html")
            
        user = db.validate_user(email, phone)
        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1] if len(user) > 1 else email
            flash("Login successful! Welcome to Prajapati Palace.", "success")
            return redirect("/user_dashboard")
        
        flash("No account found. Please register.", "danger")
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect("/login")


@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/login")
    return render_template("admin_dashboard.html")

@app.route("/user_dashboard")
def user_dashboard():
    if "user_id" not in session:
        return redirect("/login")
    user_id = session["user_id"]
    bookings = db.get_bookings_by_guest(user_id)
    return render_template("user_dashboard.html", username=session.get("user_name"), bookings=bookings)


@app.route("/users")
def users():
    if "admin" not in session:
        return redirect("/login")
    data = db.get_all_users()
    return render_template("manage_users.html", users=data)

@app.route("/add_user", methods=["POST"])
def add_user():
    if "admin" not in session:
        return redirect("/login")
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    address = request.form.get("address")
    db.insert_user(name, phone, email, address)
    flash("User added successfully", "success")
    return redirect("/users")

@app.route("/delete_user/<int:id>")
def delete_user(id):
    if "admin" not in session:
        return redirect("/login")
    db.delete_user(id)
    flash("User deleted", "info")
    return redirect("/users")


@app.route("/admin/bookings")
def admin_bookings():
    if "admin" not in session:
        return redirect("/login")
    bookings = db.get_all_bookings()
    return render_template("admin_booking.html", bookings=bookings)

@app.route("/admin/create_booking", methods=["GET","POST"])
def admin_create_booking():
    if "admin" not in session:
        return redirect("/login")
    if request.method == "POST":
        guest_id = int(request.form["guest_id"])
        room_id = int(request.form["room_id"])
        check_in = request.form["check_in"]
        check_out = request.form["check_out"]
        bid = db.create_booking(guest_id, room_id, check_in, check_out, status='Confirmed')
        if not bid:
            flash("Room not available for chosen dates", "danger")
            return redirect(url_for("admin_create_booking"))
        flash(f"Booking #{bid} created", "success")
        return redirect("/admin/bookings")
    guests = db.get_all_users()
    rooms = db.get_all_rooms()
    return render_template("admin_create_booking.html", guests=guests, rooms=rooms)

@app.route("/admin/update_booking/<int:booking_id>", methods=["POST"])
def admin_update_booking(booking_id):
    if "admin" not in session:
        return redirect("/login")
    new_status = request.form.get("status")
    db.update_booking_status(booking_id, new_status)
    flash("Booking status updated", "success")
    return redirect("/admin/bookings")

# Payments
@app.route("/admin/payments")
def admin_payments():
    if "admin" not in session:
        return redirect("/login")
    payments = db.get_all_payments()
    return render_template("admin_payments.html", payments=payments)

# Public Rooms
@app.route("/rooms")
def rooms():
    rooms = db.get_all_rooms()
    return render_template("rooms.html", rooms=rooms)

@app.route("/register")
def register():
    flash("Please contact admin to register.", "info")
    return redirect("/login")

# User Booking
@app.route("/book", methods=["GET","POST"])
def book():
    if "user_id" not in session:
        flash("Please log in to book a room.", "warning")
        return redirect("/login")
    if request.method == "POST":
        guest_id = session["user_id"]
        room_id = int(request.form["room_id"])
        check_in = request.form["check_in"]
        check_out = request.form["check_out"]
        bid = db.create_booking(guest_id, room_id, check_in, check_out, status='Confirmed')
        if not bid:
            flash("Room not available", "danger")
            return redirect(url_for("book"))
        flash(f"Booking confirmed! ID: {bid}", "success")
        return redirect("/user_dashboard")
    
    today = datetime.today().date()
    # Simple logic for future date
    future = today 
    rooms = db.get_available_rooms(str(today), str(future))
    return render_template("booking.html", rooms=rooms)

# app.py (Updated Payment Section)

# ... (Previous code remains the same) ...

# ==========================================
# PAYMENT LOGIC (FIXED)
# ==========================================

@app.route("/booking/<int:booking_id>/payments")
def booking_payments(booking_id):
    # Allow BOTH User and Admin to view payments
    if "user_id" not in session and "admin" not in session:
        return redirect("/login")
        
    payments = db.get_payments_by_booking(booking_id)
    return render_template("payments.html", payments=payments, booking_id=booking_id)

@app.route("/make_payment/<int:booking_id>", methods=["GET","POST"])
def make_payment(booking_id):
    # FIX: Allow BOTH User and Admin to access this page
    if "user_id" not in session and "admin" not in session:
        flash("Please log in to make a payment.", "warning")
        return redirect("/login")
        
    if request.method == "POST":
        # Capture Amount & Method
        amount = float(request.form["amount"])
        method = request.form["method"]
        pay_date = request.form.get("payment_date") or datetime.today().strftime("%Y-%m-%d")
        
        # Note: In a real app, you would process card_number, expiry, cvv here.
        # For now, we just insert the record into the database.
        
        pid = db.insert_payment(booking_id, amount, pay_date, method)
        flash(f"Payment Successful! Transaction ID: {pid}", "success")
        return redirect(f"/booking/{booking_id}/payments")
        
    return render_template("make_payment.html", booking_id=booking_id)

if __name__ == "__main__":
    app.run(debug=True)