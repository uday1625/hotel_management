
import mysql.connector as myconn
import config
from datetime import datetime

db = myconn.connect(
    host="localhost",
    user="root",
    password="root",
    database="Hotel"
)
cursor = db.cursor(buffered=True)


def insert_user(name, phone, email, address):
    query = "INSERT INTO Guest (Name, Phone, Email, Address) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, phone, email, address))
    db.commit()
    return cursor.lastrowid

def get_all_users():
    cursor.execute("SELECT * FROM Guest")
    return cursor.fetchall()

def search_user(name):
    cursor.execute("SELECT * FROM Guest WHERE Name LIKE %s", ("%" + name + "%",))
    return cursor.fetchall()

def update_user(id, name, phone, email, address):
    query = "UPDATE Guest SET Name=%s, Phone=%s, Email=%s, Address=%s WHERE Guest_ID=%s"
    cursor.execute(query, (name, phone, email, address, id))
    db.commit()

def delete_user(id):
    cursor.execute("DELETE FROM Guest WHERE Guest_ID=%s", (id,))
    db.commit()


def validate_admin(username, password):
    # demo: check Admins table
    cursor.execute("SELECT * FROM Admins WHERE Username=%s AND Password=%s", (username, password))
    return cursor.fetchone() is not None

def validate_user(email, phone):
    cursor.execute("SELECT * FROM Guest WHERE Email=%s AND Phone=%s", (email, phone))
    return cursor.fetchone()

def get_all_rooms():
    cursor.execute("SELECT * FROM Room")
    return cursor.fetchall()

def get_available_rooms(start_date, end_date):
    """
    Return rooms that have no overlapping confirmed bookings between start_date and end_date.
    """
    query = """
    SELECT r.* FROM Room r
    WHERE r.Room_ID NOT IN (
        SELECT b.Room_ID FROM Booking b
        WHERE NOT (b.Check_Out_Date <= %s OR b.Check_IN_Date >= %s)
        AND b.Status IN ('Confirmed','Completed')
    )
    AND r.Status = 'Available'
    """
    cursor.execute(query, (start_date, end_date))
    return cursor.fetchall()

def get_room_by_id(room_id):
    cursor.execute("SELECT * FROM Room WHERE Room_ID=%s", (room_id,))
    return cursor.fetchone()

def update_room_status(room_id, status):
    cursor.execute("UPDATE Room SET Status=%s WHERE Room_ID=%s", (status, room_id))
    db.commit()


def create_booking(guest_id, room_id, check_in, check_out, status='Confirmed'):
    # Basic overlap check
    query = """
    SELECT COUNT(*) FROM Booking b
    WHERE b.Room_ID=%s AND NOT (b.Check_Out_Date <= %s OR b.Check_IN_Date >= %s)
    AND b.Status IN ('Confirmed','Completed')
    """
    cursor.execute(query, (room_id, check_in, check_out))
    conflict = cursor.fetchone()[0]
    if conflict > 0:
        return None  # room not available

    cursor.execute("SELECT IFNULL(MAX(Booking_ID),0) FROM Booking")
    maxid = cursor.fetchone()[0] or 0
    new_id = maxid + 1
    insert_q = """INSERT INTO Booking (Booking_ID, Guest_ID, Room_ID, Check_IN_Date, Check_Out_Date, Status)
                  VALUES (%s,%s,%s,%s,%s,%s)"""
    cursor.execute(insert_q, (new_id, guest_id, room_id, check_in, check_out, status))
    update_room_status(room_id, 'Booked')
    db.commit()
    return new_id

def get_bookings_by_guest(guest_id):
    cursor.execute("SELECT b.*, r.Room_Number, r.Price FROM Booking b LEFT JOIN Room r ON b.Room_ID=r.Room_ID WHERE b.Guest_ID=%s ORDER BY b.Check_IN_Date DESC", (guest_id,))
    return cursor.fetchall()

def get_all_bookings():
    cursor.execute("SELECT b.*, g.Name AS GuestName, r.Room_Number FROM Booking b LEFT JOIN Guest g ON b.Guest_ID=g.Guest_ID LEFT JOIN Room r ON b.Room_ID=r.Room_ID ORDER BY b.Check_IN_Date DESC")
    return cursor.fetchall()

def get_booking_by_id(booking_id):
    cursor.execute("SELECT * FROM Booking WHERE Booking_ID=%s", (booking_id,))
    return cursor.fetchone()

def update_booking_status(booking_id, status):
    b = get_booking_by_id(booking_id)
    if not b:
        return False
    cursor.execute("UPDATE Booking SET Status=%s WHERE Booking_ID=%s", (status, booking_id))
    if status in ('Cancelled','Completed'):
        room_id = b[2]
        update_room_status(room_id, 'Available')
    db.commit()
    return True

def insert_payment(booking_id, amount, payment_date, payment_method):
    cursor.execute("SELECT IFNULL(MAX(Payment_ID),0) FROM Payment")
    maxid = cursor.fetchone()[0] or 0
    new_id = maxid + 1
    q = "INSERT INTO Payment (Payment_ID, Booking_ID, Amount, Payment_date, Payment_method) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(q, (new_id, booking_id, amount, payment_date, payment_method))
    db.commit()
    return new_id

def get_payments_by_booking(booking_id):
    cursor.execute("SELECT * FROM Payment WHERE Booking_ID=%s", (booking_id,))
    return cursor.fetchall()

def get_all_payments():
    cursor.execute("SELECT p.*, b.Guest_ID FROM Payment p LEFT JOIN Booking b ON p.Booking_ID=b.Booking_ID ORDER BY p.Payment_date DESC")
    return cursor.fetchall()
