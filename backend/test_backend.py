import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app


class TestLostAndFoundBackend(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.supabase_patch = patch("backend.main.supabase", object())
        self.supabase_patch.start()

    def tearDown(self):
        self.supabase_patch.stop()

    @patch("backend.main.items.create_item")
    def test_create_item(self, mock_create_item):
        mock_create_item.return_value = {
            "id": 1,
            "type": "lost",
            "title": "Wallet",
            "description": "Black wallet",
            "location": "Library",
            "status": "active",
        }

        response = self.client.post(
            "/items/",
            json={
                "type": "Lost",
                "name": "Wallet",
                "description": "Black wallet",
                "location": "Library",
            },
        )

        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["name"], "Wallet")
        self.assertEqual(body["status"], "active")

    @patch("backend.main.items.fetch_items")
    def test_retrieve_items(self, mock_fetch_items):
        mock_fetch_items.return_value = [
            {
                "id": 1,
                "type": "found",
                "title": "Bottle",
                "description": "Blue bottle",
                "location": "Cafeteria",
                "status": "active",
            }
        ]

        response = self.client.get("/items/")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["name"], "Bottle")

    @patch("backend.main.items.fetch_items")
    def test_search_items(self, mock_fetch_items):
        mock_fetch_items.return_value = []

        response = self.client.get("/items/?query=wallet")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
        _, kwargs = mock_fetch_items.call_args
        self.assertEqual(kwargs["search_query"], "wallet")

    @patch("backend.main.items.update_item_status")
    def test_update_status(self, mock_update_status):
        mock_update_status.return_value = {
            "id": 1,
            "type": "lost",
            "title": "Wallet",
            "status": "resolved",
        }

        response = self.client.patch("/items/1/status", json={"status": "Returned"})

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "resolved")


if __name__ == "__main__":
    unittest.main()
