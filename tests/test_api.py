import pytest


class TestLogin:


    @pytest.mark.parametrize("email, password, output", [
        ("abc@google.com", "123", 200)  # happy case
    ])
    def test_login_success(self, server, email, password, output):
        payload: dict = {"email": email, "password": password}
        result = server.post("/api/auth/login", json=payload, content_type="application/json") 
        assert result.status_code == output
        assert set(result.json) == set(["data", "message", "success"])
        assert "token" in result.json["data"]
        assert type(result.json["data"]["token"]) == str
        assert len(result.json["data"]["token"]) != 0

    
    @pytest.mark.parametrize("email, password, output", [
        ("abc@google.com", "345", 404),  # correct email, wrong password
        ("a@google.com", "123", 404),  # wrong email, correct password
        ("abc@google.com", "", 404)  # wrong email, empty password
    ])
    def test_login_fail_wrong_creds(self, server, email, password, output):
        payload: dict = {"email": email, "password": password}
        result = server.post("/api/auth/login", json=payload, content_type="application/json") 
        assert result.status_code == output
        assert set(result.json) == set(["data", "message", "success"])
        assert result.json["data"] == {}  # no data is passed when the login fails


    @pytest.mark.parametrize("email, password, output", [
        ("", "123", 400),  # empty email, should have email-like input
    ])
    def test_login_fail_violate_validation(self, server, email, password, output):
        payload: dict = {"email": email, "password": password}
        result = server.post("/api/auth/login", json=payload, content_type="application/json") 
        assert result.status_code == output
        assert set(result.json) == set(["data", "message", "success"])   # making sure that the response is standardized
        assert result.json["data"] == {}  # no data is passed when the login fails


class TestSignup:


    @pytest.mark.parametrize("email, username, password, output", [
        ("cde@yahoo.com", "cde", "aBc1_", 200)
    ])
    def test_signup_success(self, server, email, username, password, output):
        payload: dict = {"email": email, "username": username, "password": password}
        result = server.post("/api/auth/signup", json=payload, content_type="application/json") 
        assert result.status_code == output
        assert set(result.json) == set(["data", "message", "success"])
        assert result.json["success"] == True


    
    @pytest.mark.parametrize("email, username, password, output", [
        ("abc@yahoo.com", "abc", "abc", 404),  # only lowercase
        ("abc@yahoo.com", "abc", "abC", 404),  # with lowercase and uppercase
        ("abc@yahoo.com", "abc", "abC1", 404),  # with lowercase, uppercase, and number
        ("abc@yahoo.com", "abc", "abC!", 404),  # with lowercase, uppercase, and special character
        ("abc@yahoo.com", "abc", "ABC1_", 404),  # with uppercase, number, and special character
        ("abc@yahoo.com", "abc", "", 404)  # empty string
    ])
    def test_signup_fail_password_not_fulfil_requirement(self, server, email, username, password, output):
        payload: dict = {"email": email, "username": username, "password": password}
        result = server.post("/api/auth/signup", json=payload, content_type="application/json") 
        assert result.status_code == output
        assert set(result.json) == set(["data", "message", "success"])
        assert result.json["success"] == False
        assert result.json["data"] == {}
        assert type(result.json["message"]) == str


    @pytest.mark.parametrize("email, username, password, output", [
        ("abc@yahoo.com", "cde", "aBc1_", 404)
    ])
    def test_signup_fail_account_already_exist(self, server, email, username, password, output):
        payload: dict = {"email": email, "username": username, "password": password}
        result = server.post("/api/auth/signup", json=payload, content_type="application/json") 
        assert result.status_code == output
        assert set(result.json) == set(["data", "message", "success"])
        assert result.json["success"] == False
        assert result.json["data"] == {}