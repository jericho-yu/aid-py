import requests
import json
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
from enum import Enum


class HttpMethods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HttpClient:
    def __init__(self, target: str):
        self.url = target
        self.method = HttpMethods.GET
        self.headers = {}
        self.params = {}
        self.data = None
        self.auth = None
        self.timeout = 0
        self.response = None

    def set_method(self, method):
        self.method = method
        return self

    def set_headers(self, headers):
        self.headers.update(headers)
        return self

    def set_params(self, params):
        self.params.update(params)
        return self

    def give_body(self, body):
        self.data = body
        return self

    def set_json_body(self, body):
        self.headers["Content-Type"] = "application/json"
        self.data = json.dumps(body)
        return self

    def set_xml_body(self, body):
        self.headers["Content-Type"] = "application/xml"
        self.data = ET.tostring(body)
        return self

    def set_auth(self, username, password):
        self.auth = HTTPBasicAuth(username, password)
        return self

    def set_timeout(self, timeout):
        self.timeout = timeout
        return self

    def send(self):
        self.response = requests.request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            params=self.params,
            data=self.data,
            auth=self.auth,
            timeout=self.timeout,
        )
        return self

    def get_response(self):
        return self.response

    def get_json_response(self):
        return self.response.json()

    def get_xml_response(self):
        return ET.fromstring(self.response.content)

    def save_response_to_file(self, filename):
        with open(filename, "wb") as file:
            file.write(self.response.content)
        return self

