import os
import tempfile
import unittest

import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()

        self.original_db_name = database.DB_NAME
        database.DB_NAME = self.temp_file.name

        database.initialize_database()

    def tearDown(self):
        database.DB_NAME = self.original_db_name
        os.unlink(self.temp_file.name)

    def test_add_application(self):
        application_id = database.add_application(
            "Test Company",
            "Backend Developer"
        )

        self.assertIsInstance(application_id, int)
        self.assertGreater(application_id, 0)

    def test_invalid_company(self):
        with self.assertRaises(ValueError):
            database.add_application("", "Backend Developer")

    def test_invalid_position(self):
        with self.assertRaises(ValueError):
            database.add_application("Test Company", "   ")

    def test_duplicate_application(self):
        database.add_application(
            "Duplicate Test Company",
            "Software Engineer"
        )

        with self.assertRaises(ValueError):
            database.add_application(
                " duplicate test company ",
                "SOFTWARE ENGINEER "
            )

    def test_different_position_is_allowed(self):
        application_id = database.add_application(
            "Duplicate Test Company",
            "Frontend Developer"
        )

        self.assertGreater(application_id, 0)


if __name__ == "__main__":
    unittest.main()