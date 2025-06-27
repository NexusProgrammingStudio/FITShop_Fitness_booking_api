# FITShop Fitness Class Booking Booking API

This is a Flask-based REST API for a fictional fitness studio that allows users to:

- View all available classes
- Book a class by providing name and email
- View all bookings for a specific email
- Automatically handles timezone conversion (IST to user’s timezone)
- Prevents overbooking and duplicate bookings

---

## Features

- Python + Flask REST API
- SQLite database (file or in-memory)
- Timezone-aware (stored in IST, converted on request)
- Prevents overbooking
- Unique constraint: one user per class
- Clean, modular code with validations
- Seed data and unit test scaffold

---

## API Endpoints

### `GET /classes?timezone=<TZ>`

Returns a list of all upcoming classes converted to the specified timezone (default: UTC).

**Example Request:**

```bash
curl http://localhost:5000/classes?timezone=Europe/London
```

**Example Response:**

```json
[
  {
    "available_slots": 5,
    "datetime": "2025-06-25T22:55:00-04:00",
    "id": 1,
    "instructor": "Aditya",
    "name": "Yoga"
  }
]

```

### `GET /book`

Creates a new booking. Requires JSON body:

**Example Request:**

```bash
curl -X POST http://localhost:5000/book \
  -H "Content-Type: application/json" \
  -d '{"class_id": 1, "client_name": "Riya", "client_email": "riya@example.com"}'

```

**Example Body:**

```json
{
  "class_id": 1,
  "client_name": "Riya",
  "client_email": "riya@example.com"
}

```

**Example Response:**

```json
{
  "booking_id": 1,
  "client_email": "riya@example.com",
  "client_name": "Riya",
  "message": "Booking successful"
}

```

### `GET bookings?email=<user_email>`

Returns all bookings made by a specific email address.

**Example Request:**

```bash
curl http://localhost:5000/bookings?email=riya@example.com
```

**Example Response:**

```json
[
  {
    "booking_id": 1,
    "class_name": "Yoga",
    "datetime": "2025-06-26T12:55:00+00:00",
    "instructor": "Aditya"
  }
]
```

### Setup

```bash
  git clone https://github.com/NexusProgrammingStudio/FITShop_Fitness_booking_api.git
  cd FITshop_fitness_booking_api  
  python -m venv .venv  
  source .venv/bin/activate  # On Windows use `venv\Scripts\activate`  
  pip install -r requirements.txt
```

### Run the Application

```bash
    python app.py
```

### Run Tests

```bash
    python tests.py
```
