from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_send_json_request1(self):
        data = {
            "key": "1.1.1.1.1.1.1",
            "items": 2,
            "mandates": [1, 1],
            "preferences": [[1, 1], [1, 1]],
        }
        response = self.client.post(
            "https://backend-vs0l.onrender.com/api/test", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "allocation": [[0, 1.0], [1.0, 0]],
                "rounded_allocation": [[0, 1.0], [1.0, 0]],
            },
        )

    def test_send_json_request2(self):
        data = {
            "key": "1.1.1.1.1.1.1",
            "items": 1,
            "mandates": [4, 3, 1],
            "preferences": [[1], [1], [1]],
        }
        response = self.client.post(
            "https://backend-vs0l.onrender.com/api/test", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "allocation": [[0.5, 0.38, 0.12]],
                "rounded_allocation": [[0.57, 0.43, 0]],
            },
        )

    def test_send_json_request3(self):
        data = {
            "key": "1.1.1.1.1.1.1",
            "items": 3,
            "mandates": [1, 2, 3],
            "preferences": [[1, 2, 3], [2, 1, 3], [3, 2, 1]],
        }
        response = self.client.post(
            "https://backend-vs0l.onrender.com/api/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, -1)

    def test_send_wrong_json_request(self):
        data = {
            "key": "1.1.1.1.1.1.1",
            "items": 3,
            "mandates": [1, 2, 3],
            "preferences": [[2, 1, 3], [3, 2, 1]],
        }
        response = self.client.post(
            "https://backend-vs0l.onrender.com/api/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Invalid Input")

    def test_send_not_json_request(self):
        data = "not json"
        response = self.client.post(
            "https://backend-vs0l.onrender.com/api/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Invalid Input")

    def test_retrieving_session(self):
        data = {
            "key": "3.3.3.3.3.3.3",
            "items": 3,
            "mandates": [1, 2, 3],
            "preferences": [[1, 2, 3], [2, 1, 3], [3, 2, 1]],
        }
        respone = self.client.post(
            "https://backend-vs0l.onrender.com/api/", data, format="json"
        )
        self.assertEqual(respone.status_code, status.HTTP_200_OK)
        data = {"key": "3.3.3.3.3.3.3"}
        respone = self.client.post(
            "https://backend-vs0l.onrender.com/api/getsave", data, format="json"
        )
        self.assertEqual(respone.status_code, status.HTTP_200_OK)
        self.assertEqual(respone.data, "[[1, 2, 3], [2, 1, 3], [3, 2, 1]]")

    def test_retrieving_nonexisting_session(self):
        data = {"key": "Not.a.key.at.all"}
        respone = self.client.post(
            "https://backend-vs0l.onrender.com/api/getsave", data, format="json"
        )
        self.assertEqual(respone.status_code, status.HTTP_200_OK)
        self.assertEqual(respone.data, -1)

    def test_retrieving_not_a_json_key_session(self):
        data = "not json"
        respone = self.client.post(
            "https://backend-vs0l.onrender.com/api/getsave", data, format="json"
        )
        self.assertEqual(respone.status_code, status.HTTP_200_OK)
        self.assertEqual(respone.data, -1)



































































