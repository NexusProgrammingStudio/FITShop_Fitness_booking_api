import unittest

from app import app


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_classes(self):
        response = self.client.get('/classes')
        self.assertEqual(response.status_code, 200)

    def test_invalid_booking(self):
        response = self.client.post('/book', json={})
        self.assertEqual(response.status_code, 400)

    def test_missing_email(self):
        response = self.client.get('/bookings')
        self.assertEqual(response.status_code, 400)

    def test_overbooking(self):
        # Book all available slots
        for _ in range(3):  # HIIT class has 3 slots
            self.client.post('/book', json={
                "class_id": 2,
                "client_name": f"Test User {_}",
                "client_email": f"test{_}@example.com"
            })
        # 4th booking should fail
        res = self.client.post('/book', json={
            "class_id": 2,
            "client_name": "Overbook",
            "client_email": "fail@example.com"
        })
        self.assertEqual(res.status_code, 409)


if __name__ == '__main__':
    unittest.main()
