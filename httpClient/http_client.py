import requests
import json
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth


class HttpClient:
    def __init__(self, url):
        self.url = url
        self.headers = {}
        self.params = {}
        self.data = None
        self.auth = None
        self.timeout = None
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

    def set_body(self, body):
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

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/items/1"
    timeout = 5
    hc = HttpClient(url).set_timeout(timeout).set_method("GET").send()
    res = hc.get_response()
    print(hc.get_json_response())