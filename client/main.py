from hashlib import md5
from urllib import request


class Client:

    def send_response(self, method, url, data):
        response = request.Request(method=method, url=url, data=data)
        return response

    def get_sign(self, data):
        pass
