import pytest
from app.utils import auth
from app.models.user import User


class TestCheckExistingUser:


    def test_existing_user_with_email_only(self, server):
        with server.app_context():
            exist_email: str = "abc@google.com"
            not_exist_email: str = "xyz@google.com"
            
            valid_email = auth.check_existing_user(email=exist_email)
            not_valid_email = auth.check_existing_user(email=not_exist_email)
            
            # HAPPY CASE
            assert valid_email == True
            # FAIL CASE
            assert not_valid_email == False
            

    def test_existing_user_with_email_and_username(self, server):
        with server.app_context():
            exist_email: str = "abc@google.com"
            exist_username: str = "abc"
            not_exist_email: str = "xyz@google.com"
            not_exist_username: str = "xyz"

            valid_email_valid_username = auth.check_existing_user(email=exist_email, username=exist_username)
            valid_email_not_valid_username =auth.check_existing_user(email=exist_email, username=not_exist_username)
            not_valid_email_valid_username =auth.check_existing_user(email=not_exist_email, username=exist_username)
            not_valid_email_not_valid_username =auth.check_existing_user(email=not_exist_email, username=not_exist_username)
            
            # HAPPY CASE
            assert valid_email_valid_username == True
            # FAIL CASE
            assert valid_email_not_valid_username == False
            assert not_valid_email_valid_username == False
            assert not_valid_email_not_valid_username == False

class TestGetUserData:


    def test_get_exist_user_data(self, server):
        with server.app_context():
            email: str = "abc@google.com"
            user_data = auth.get_user_data(email=email)

            assert type(user_data) == User
            assert hasattr(user_data, "email") == True
            assert hasattr(user_data, "username") == True
            assert hasattr(user_data, "salt") == True
            assert hasattr(user_data, "hash") == True

    def test_get_not_exist_user_data(self, server):
        with server.app_context():
            email: str = "xyz@google.com"
            user_data = auth.get_user_data(email=email)
            
            assert user_data is None

