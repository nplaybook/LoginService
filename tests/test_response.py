import pytest

from app.utils import response

class TestGenerateResponse:


    @pytest.mark.parametrize("http_status, message, data, output", [
        (200, "this is a message", "this is data", dict),  # input all parameters
        (201, "this is a message", None, dict), # not input data param
        ("200", "this is a message", "this is data", dict),  # input all parameters, status code in string
        ("200", "this is a message", None, dict),  # not input data param, status code in string
        
    ])
    def test_http_status_200(self, http_status, message, data, output):
        result = response.generate_response(http_status, message, data)
        assert type(result) == output
        assert result["success"] is True

    @pytest.mark.parametrize("http_status, message, data, output", [
        (400, "this is a message", "this is data", dict),  # input all parameters
        (301, "this is a message", None, dict), # not input data param
        ("400", "this is a message", "this is data", dict),  # input all parameters, status code in string
        ("501", "this is a message", None, dict),  # not input data param, status code in string
    ])
    def test_http_status_not_200(self, http_status, message, data, output):
        result = response.generate_response(http_status, message, data)
        assert type(result) == output
        assert result["success"] is False