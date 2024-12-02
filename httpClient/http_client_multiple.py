from concurrent.futures import ThreadPoolExecutor

import requests


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

    def set_auth(self, username, password):
        self.auth = (username, password)
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

class HttpClientMultiple:
    def __init__(self):
        self.clients = []

    def add(self, client):
        self.clients.append(client)
        return self

    def set_clients(self, clients):
        self.clients = clients
        return self

    def send(self):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(client.send) for client in self.clients]
            for future in futures:
                future.result()
        return self

    def get_clients(self):
        return self.clients