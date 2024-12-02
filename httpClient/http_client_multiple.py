import threading
from httpClient.http_client import HttpClient

class HttpClientMultiple:
    def __init__(self):
        self.clients = []

    def add(self, hc):
        self.clients.append(hc)
        return self

    def set_clients(self, clients):
        self.clients = clients
        return self

    def send(self):
        if len(self.clients) > 0:
            threads = []
            for client in self.clients:
                thread = threading.Thread(target=client.send)
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
        return self

    def get_clients(self):
        return self.clients

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/items/1"
    timeout = 5
    hc = HttpClient(url).set_timeout(timeout).set_method("GET").send()
    hcm = HttpClientMultiple()
    hcm.add(hc).send()
    for i in hcm.get_clients():
        print(i.get_json_response())