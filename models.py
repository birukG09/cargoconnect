from datetime import datetime 
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User model representing system users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the user
    email = db.Column(db.String(120), unique=True, nullable=False)  # User email, must be unique
    password_hash = db.Column(db.String(256))  # Hashed password for security
    name = db.Column(db.String(100), nullable=False)  # Full name of the user
    role = db.Column(db.String(20), nullable=False)  # User role: customer, transporter, or admin
    phone = db.Column(db.String(20))  # Contact phone number
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of account creation

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

# Booking model representing cargo transport orders
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the booking
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Customer making the booking
    transporter_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Assigned transporter
    pickup_location = db.Column(db.String(200), nullable=False)  # Pickup address
    delivery_location = db.Column(db.String(200), nullable=False)  # Delivery address
    cargo_type = db.Column(db.String(100), nullable=False)  # Type of cargo
    weight = db.Column(db.Float, nullable=False)  # Weight of the cargo in kg
    status = db.Column(db.String(20), default='pending')  # Status: pending, accepted, in_transit, delivered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Booking creation timestamp
    estimated_price = db.Column(db.Float, nullable=False)  # Estimated transport cost

    customer = db.relationship('User', foreign_keys=[customer_id])  # Relationship with customer
    transporter = db.relationship('User', foreign_keys=[transporter_id])  # Relationship with transporter

# Payment model representing transaction details
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the payment
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)  # Associated booking
    amount = db.Column(db.Float, nullable=False)  # Payment amount
    status = db.Column(db.String(20), default='pending')  # Payment status: pending, completed, failed
    payment_method = db.Column(db.String(20), nullable=False)  # Payment method: chapa, telebirr
    transaction_id = db.Column(db.String(100))  # Transaction reference ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of payment creation

    booking = db.relationship('Booking')  # Relationship with booking

# Location model for tracking cargo movement
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for location tracking
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)  # Associated booking
    latitude = db.Column(db.Float, nullable=False)  # Latitude coordinate
    longitude = db.Column(db.Float, nullable=False)  # Longitude coordinate
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Time of location update

    booking = db.relationship('Booking')  # Relationship with booking
