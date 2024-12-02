import threading


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
