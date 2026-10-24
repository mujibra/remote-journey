import unittest


def add_application(application):
    company = application.get("company")
    position = application.get("position")

    if not isinstance(company, str) or not company.strip():
        raise ValueError("Company name is required")

    if not isinstance(position, str) or not position.strip():
        raise ValueError("Position is required")

    return application

def is_duplicate(applications, new_application):
    for application in applications:
        existing_company = application["company"].strip().lower()
        new_company = new_application["company"].strip().lower()

        existing_position = application["position"].strip().lower()
        new_position = new_application["position"].strip().lower()

        if existing_company == new_company and existing_position == new_position:
            return True

        return False
    
ALLOWED_STATUSES = {"Applied", "Interview", "Rejected", "Accepted"}

def update_status(application, new_status):

    if new_status not in ALLOWED_STATUSES:
        raise ValueError("Invalid application status")

    application["status"] = new_status

    return application
    
class TestAddApplication(unittest.TestCase):

    def test_valid_company(self):
        application = {
            "company": "Google",
            "position": "Software Engineer"
        }

        result = add_application(application)

        self.assertEqual(result, application)

    def test_empty_company(self):
        application = {
            "company": "",
            "position": "Software Engineer"
        }

        with self.assertRaises(ValueError):
            add_application(application)

    def test_empty_position(self):
        application = {
            "company": "Google",
            "position": ""
        }

        with self.assertRaises(ValueError):
            add_application(application)

    def test_missing_company(self):
        application = {
            "position": "Software Engineer"
        }

        with self.assertRaises(ValueError):
            add_application(application)

    def test_is_duplicate(self):
        application = [
            {"company": " google ", "position": "SOFTWARE Engineer "},  
        ]
        new_application = {
            "company": "Google", 
            "position": "Software Engineer"
        }

        result = is_duplicate(application, new_application)

        self.assertTrue(result)

    def test_update_status(self):
        application = {
            "company": "Google",
            "position": "Software Engineer",
            "status": "Applied"
        }

        result = update_status(application, "Interview")

        self.assertEqual(result["status"], "Interview")


    def test_invalid_status(self):
        application = {
            "company": "Google",
            "position": "Software Engineer",
            "status": "Applied"
        }

        with self.assertRaises(ValueError):
            update_status(application, "Maybe")

application = {"status": "Applied"}
update_status(application, "Interview")

print(application)

if __name__ == "__main__":
    unittest.main()