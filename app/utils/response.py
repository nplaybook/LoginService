def generate_response(http_status: int, message: str, data: dict=None) -> dict:
    """Generate json format as a return if
    api request is successful or fail.

    :param http_status: {int} http status code in 2** family if success,
    4** if error from the client side, and 500 if error from server side.
    :param message: {str} short description of the response
    :param data: {dict} json data that will be used in client side. If response
    fail, doesn't have to pass this param
    
    :return: {dict}
    """

    dict_result = {
        "message": message,
        "data": {}
    }

    dict_result["success"] = True if str(http_status)[0] == "2" else False
    if data: dict_result["data"] = data
    return dict_result