from datetime import datetime, UTC

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FitnessActivityClasses(db.Model):
    __tablename__ = 'fitness_activity_class'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    datetime_ist = db.Column(db.DateTime, nullable=False)
    instructor = db.Column(db.String(80), nullable=False)
    available_bookable_slots = db.Column(db.Integer, nullable=False, default=5)


class Booking(db.Model):
    __tablename__ = 'booking'
    __table_args__ = (
        db.UniqueConstraint('client_email', 'class_id', name='unique_booking_per_user_per_class'),
    )
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(80), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('fitness_activity_class.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(UTC))


def init_db(app):
    with app.app_context():
        db.create_all()
        if not FitnessActivityClasses.query.first():
            from pytz import timezone
            ist = timezone('Asia/Kolkata')
            now = datetime.now(ist).replace(second=0, microsecond=0)
            db.session.add_all([
                FitnessActivityClasses(name="Yoga", datetime_ist=now.replace(hour=8), instructor="Aditya",
                                       available_bookable_slots=5),
                FitnessActivityClasses(name="HIIT", datetime_ist=now.replace(hour=10), instructor="Bhavik",
                                       available_bookable_slots=3),
                FitnessActivityClasses(name="Zumba", datetime_ist=now.replace(hour=18), instructor="Charu",
                                       available_bookable_slots=2),
                FitnessActivityClasses(name="Pilates", datetime_ist=now.replace(hour=20), instructor="David",
                                       available_bookable_slots=4),
                FitnessActivityClasses(name="Cardio", datetime_ist=now.replace(hour=22), instructor="Meelu",
                                       available_bookable_slots=6),
            ])
            db.session.commit()
