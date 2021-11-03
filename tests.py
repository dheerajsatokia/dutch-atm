import unittest
import json
from app import app, db


class AtmTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db.session

    def get_atms(self):
        response = self.app.get('/atms', headers={"Content-Type": "application/json"})
        print(response)
        self.assertEqual(list, type(response.json['data']))
        self.assertEqual(200, response.status_code)

    def update_atms(self):
        payload = json.dumps({
            "distance": 5,
        })

        response = self.app.put('atms/update?atm_id=4', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(str, type(response.json['data']))
        self.assertEqual(200, response.status_code)
