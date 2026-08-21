import os
import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Mock the Supabase client connection BEFORE importing app.
mock_supabase = MagicMock()

# Setup a robust reusable query builder mock
mock_query = MagicMock()
mock_query.eq.return_value = mock_query
mock_query.order.return_value = mock_query
mock_query.or_.return_value = mock_query

mock_supabase.table.return_value.select.return_value = mock_query
mock_supabase.table.return_value.insert.return_value = mock_query
mock_supabase.table.return_value.update.return_value = mock_query

with patch("backend.supabase_client.supabase", mock_supabase):
    from backend.main import app

client = TestClient(app)

class TestLostAndFoundBackend(unittest.TestCase):
    @patch("backend.main.supabase", mock_supabase)
    def test_add_item(self):
        # Configure mock return data for insert
        mock_query.execute.return_value.data = [
            {
                "id": 1,
                "type": "lost",
                "title": "Lost iPhone",
                "description": "Black iPhone 13 in library",
                "category": "Electronics",
                "location": "Library Room 3",
                "date": "2026-08-21",
                "image": "https://res.cloudinary.com/demo/image/upload/sample.jpg",
                "contact_email": "john.doe@college.edu",
                "status": "active"
            }
        ]

        res = client.post("/items/", json={
            "type": "lost",
            "title": "Lost iPhone",
            "description": "Black iPhone 13 in library",
            "category": "Electronics",
            "location": "Library Room 3",
            "date": "2026-08-21",
            "image": "https://res.cloudinary.com/demo/image/upload/sample.jpg",
            "contact_email": "john.doe@college.edu"
        })

        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["title"], "Lost iPhone")
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["status"], "active")

    @patch("backend.main.supabase", mock_supabase)
    def test_list_items(self):
        # Configure mock return data for select query chain
        mock_query.execute.return_value.data = [
            {
                "id": 1,
                "type": "lost",
                "title": "Lost iPhone",
                "status": "active"
            }
        ]

        res = client.get("/items/?type=lost&status=active")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Lost iPhone")

    @patch("backend.main.supabase", mock_supabase)
    def test_patch_item_status(self):
        # Configure mock return data for update query chain
        mock_query.execute.return_value.data = [
            {
                "id": 1,
                "type": "lost",
                "title": "Lost iPhone",
                "status": "resolved"
            }
        ]

        res = client.patch("/items/1/status", json={"status": "resolved"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "resolved")

    def test_invalid_item_type(self):
        res = client.post("/items/", json={
            "type": "invalid_type",
            "title": "Lost iPhone",
            "category": "Electronics",
            "location": "Library Room 3",
            "date": "2026-08-21",
            "contact_email": "john.doe@college.edu"
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("Type must be either", res.json()["detail"])

if __name__ == "__main__":
    unittest.main()
