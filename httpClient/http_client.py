import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart.encoder import MultipartEncoder

class HttpClient:
    def __init__(self, url):
        self.url = url
        self.method = 'GET'
        self.headers = {}
        self.params = {}
        self.data = None
        self.auth = None
        self.timeout = None
        self.response = None

    def set_method(self, method):
        self.method = method.upper()
        return self

    def add_headers(self, headers):
        self.headers.update(headers)
        return self

    def set_params(self, params):
        self.params = params
        return self

    def set_body(self, body):
        self.data = body
        return self

    def set_json_body(self, body):
        self.headers['Content-Type'] = 'application/json'
        self.data = body
        return self

    def set_form_body(self, body):
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.data = body
        return self

    def set_form_data_body(self, texts, files):
        m = MultipartEncoder(fields={**texts, **{k: (v, open(v, 'rb')) for k, v in files.items()}})
        self.headers['Content-Type'] = m.content_type
        self.data = m
        return self

    def set_auth(self, username, password):
        self.auth = HTTPBasicAuth(username, password)
        return self

    def set_timeout(self, timeout):
        self.timeout = timeout
        return self

    def send(self):
        try:
            self.response = requests.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                params=self.params,
                data=self.data,
                auth=self.auth,
                timeout=self.timeout
            )
            self.response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        return self

    def get_response(self):
        return self.response

    def get_response_json(self):
        try:
            return self.response.json()
        except ValueError:
            return None

    def get_response_text(self):
        return self.response.text

    def save_response_to_file(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.response.content)