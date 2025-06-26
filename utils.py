import re

from dateutil import tz


def convert_ist_to_tz(ist_dt, target_tz_str):
    ist = tz.gettz("Asia/Kolkata")
    target = tz.gettz(target_tz_str)
    return ist_dt.replace(tzinfo=ist).astimezone(target)


def validate_booking_input(data):
    if not data:
        return False, "Request must be JSON"
    required_fields = ['class_id', 'client_name', 'client_email']
    for field in required_fields:
        if field not in data:
            return False, f"{field} is required"
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data['client_email']):
        return False, "Invalid email format"
    return True, ""
