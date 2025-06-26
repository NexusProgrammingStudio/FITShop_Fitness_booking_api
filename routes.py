import logging

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from db import db, FitnessActivityClasses, Booking
from utils import convert_ist_to_tz, validate_booking_input

api = Blueprint("api", __name__)

# Basic config: logs to console with INFO level
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)


@api.route("/", methods=["GET"])
def index():
    """
    Index route for the Fitness Class Booking API.
    """
    return jsonify({"message": "Welcome to the FITShop Fitness Class Booking API"}), 200


@api.route("/health-check", methods=["GET"])
def health_check():
    """
    Health check route for the Fitness Class Booking API.
    """
    return jsonify({"message": "Welcome to the Fitness Class Health Check API, API is Running Good."}), 200


@api.route("/classes", methods=["GET"])
def get_classes():
    """
    Get all fitness classes with their details.
    """
    logger.info("Received class view request")
    target_tz = request.args.get("timezone", "UTC")
    classes = FitnessActivityClasses.query.all()
    result = []
    for c in classes:
        local_time = convert_ist_to_tz(c.datetime_ist, target_tz)
        result.append({
            "id": c.id,
            "name": c.name,
            "datetime": local_time.isoformat(),
            "instructor": c.instructor,
            "available_slots": c.available_bookable_slots
        })
    return jsonify(result)


@api.route("/book", methods=["POST"])
def book_class():
    """
    Book a fitness class.
    """
    data = request.get_json()
    logger.info("Received booking request: %s", data)
    valid, message = validate_booking_input(data)
    if not valid:
        return jsonify({"error": message}), 400
    try:
        fitness_class = FitnessActivityClasses.query.get(data['class_id'])
        if not fitness_class:
            return jsonify({"error": "Class not found"}), 404
        if fitness_class.available_bookable_slots <= 0:
            return jsonify({"error": "No available slots"}), 409

        booking = Booking(
            client_name=data['client_name'],
            client_email=data['client_email'],
            class_id=fitness_class.id
        )
        fitness_class.available_bookable_slots -= 1
        db.session.add(booking)
        db.session.commit()

        return jsonify({"message": "Booking successful", "booking_id": booking.id, "client_name": booking.client_name,
                        "client_email": booking.client_email}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User already registered for this class"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Booking failed", "details": str(e)}), 500


@api.route("/bookings", methods=["GET"])
def get_bookings():
    """
    Get all bookings for a specific email address.
    """
    email = request.args.get("email")
    logger.info("Received booking view request from : %s", email)
    if not email:
        return jsonify({"error": "email query parameter is required"}), 400

    bookings = Booking.query.filter_by(client_email=email).all()
    result = []
    if not bookings:
        return jsonify({"error": "No bookings found for this email, Please check the address used for booking"}), 404
    for b in bookings:
        cls = FitnessActivityClasses.query.get(b.class_id)
        result.append({
            "class_name": cls.name,
            "instructor": cls.instructor,
            "datetime": convert_ist_to_tz(cls.datetime_ist, "UTC").isoformat(),
            "booking_id": b.id,
        })
    return jsonify(result)
