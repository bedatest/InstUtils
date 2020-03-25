class InvalidLoginOrPassword(Exception):
    pass

class SavedSessionNotFound(Exception):
    pass

class SaveSessionException(Exception):
    pass

class RequestException(Exception):
    def __init__(self, response, request_args):
        status_info = f"\n{response.status_code}  {response.reason}\n"
        request_info = f"Request Info:\nURL: {response.url}\n"
        request_args_info = f"Requests Args:\n{request_args}\n"
        headers_info = f"Headers:\n{response.headers}\n"

        msg = status_info + request_info + request_args_info +  headers_info

        print(msg)
        