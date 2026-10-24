import os
import tempfile
import unittest

from fastapi.testclient import TestClient
import database
from main import app


class TestJobApplicationAPI(unittest.TestCase):

    def setUp(self):
        # Give each test its own isolated database.
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()

        self.original_db_name = database.DB_NAME
        database.DB_NAME = self.temp_file.name

        database.initialize_database()
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        database.DB_NAME = self.original_db_name
        os.unlink(self.temp_file.name)

    def test_create_application(self):
        response = self.client.post(
            "/applications",
            json={
                "company": "Google",
                "position": "Backend Engineer"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["company"], "Google")
        self.assertEqual(response.json()["status"], "Applied")

    def test_list_applications(self):
        self.client.post(
            "/applications",
            json={
                "company": "Google",
                "position": "Backend Engineer"
            }
        )

        response = self.client.get("/applications")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_duplicate_application(self):
        payload = {
            "company": "Google",
            "position": "Backend Engineer"
        }

        first = self.client.post("/applications", json=payload)
        second = self.client.post(
            "/applications",
            json={
                "company": " google ",
                "position": "BACKEND ENGINEER"
            }
        )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 409)

    def test_update_status(self):
        created = self.client.post(
            "/applications",
            json={
                "company": "Google",
                "position": "Backend Engineer"
            }
        )
        application_id = created.json()["id"]

        response = self.client.patch(
            f"/applications/{application_id}",
            json={"status": "Interview"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Interview")

    def test_invalid_status(self):
        created = self.client.post(
            "/applications",
            json={
                "company": "Google",
                "position": "Backend Engineer"
            }
        )
        application_id = created.json()["id"]

        response = self.client.patch(
            f"/applications/{application_id}",
            json={"status": "Maybe"}
        )

        self.assertEqual(response.status_code, 422)

    def test_update_missing_application(self):
        response = self.client.patch(
            "/applications/99999",
            json={"status": "Interview"}
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_application(self):
        created = self.client.post(
            "/applications",
            json={
                "company": "Google",
                "position": "Backend Engineer"
            }
        )
        application_id = created.json()["id"]

        response = self.client.delete(
            f"/applications/{application_id}"
        )

        self.assertEqual(response.status_code, 204)

        listing = self.client.get("/applications")
        self.assertEqual(listing.json(), [])

    def test_delete_missing_application(self):
        response = self.client.delete("/applications/99999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()