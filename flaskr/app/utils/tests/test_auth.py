import unittest
from flaskr.app.utils import auth

class TestCheckExistingUser(unittest.TestCase):

    # PARAMETER INPUT
    def test_input_email_and_username(self):
        self.assertEqual(auth.check_existing_user(email="abc@gogle.com", username="abc"), True)

    def test_input_email_only():
        pass

    def test_input_username_only():
        pass

    # EXIST - NOT EXIST DATA INPUT
    def test_existing_account(self):
        self.assertEqual(auth.check_existing_user(email="abc@gogle.com", username="abc"), True)
        self.assertEqual(auth.check_existing_user(email="abc@gogle.com", username="cde"), False)
        self.assertEqual(auth.check_existing_user(email="abc@yaho.com", username="abc"), False)
