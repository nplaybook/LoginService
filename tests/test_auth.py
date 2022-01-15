import pytest
from app.utils import auth
from app.models.user import User


class TestCheckExistingUser:


    @pytest.mark.parametrize("email, output", [
        ("abc@google.com", True)
    ])
    def test_existing_user_email_only(self, server, email, output):
        with server.app_context():
            
            result = auth.check_existing_user(email)
            assert result == output

    @pytest.mark.parametrize("email, output", [
        ("xyz@google.com",  False),
        ("", False)
    ])
    def test_non_existing_user_email_only(self, server, email, output):
        with server.app_context():
            result = auth.check_existing_user(email)
            assert result == output

    @pytest.mark.parametrize("email, username, output", [
        ("abc@google.com", "abc", True)
    ])
    def test_existing_user_with_email_and_username(self, server, email, username, output):
        with server.app_context():
            result = auth.check_existing_user(email, username)
            assert result == output

    @pytest.mark.parametrize("email, username, output", [
        ("xyz@google.com", "xyz", False),  # not valid email - not valid username
        ("abc@google.com", "xyz", False),  # valid email - not valid username 
        ("xyz@google.com", "abc", False),  # not valid email - valid username
        ("xyz@google.com", "", False),  # not valid email - empty username
        ("", "abc", False),  # empty email - valid username
    ])
    def test_non_existing_user_with_email_and_username(self, server, email, username, output):
        with server.app_context():
            result = auth.check_existing_user(email, username)
            assert result == output


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

    @pytest.mark.parametrize("email, output", [
        ("xyz@google.com", None),
        ("", None)
    ])
    def test_get_not_exist_user_data(self, server, email, output):
        with server.app_context():
            user_data = auth.get_user_data(email)
            assert user_data == output


class TestValidatePasswordReq:


    @pytest.mark.parametrize("password, output", [
        ("Test123!", True),
        ("qweRty001_", True)
    ])
    def test_password_fulfil_requirement(self, password, output):
        result = auth.validate_password_req(password)
        assert result == output

    @pytest.mark.parametrize("password, output", [
        ("test", False),  # only lowercase
        ("tesT", False),  # with lowercase and uppercase
        ("tesT1", False),  # with lowercase, uppercase, and number
        ("tesT_", False),  # with lowercase, uppercase, and special character
        ("TEST1_", False),  # with uppercase, number, and special character
        ("", False)  # empty string
    ])
    def test_password_notfulfil_requirement(self, password, output):
        result = auth.validate_password_req(password)
        assert  result == output

