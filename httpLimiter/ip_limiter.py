import time
from threading import RLock


def new_ip_limiter() -> "IpLimiter":
    return IpLimiter()


class Visiter:
    def __init__(self):
        self.last_visit = time.time()
        self.visit_times = 1


class IpLimiter:
    def __init__(self):
        self.visit_map = {}
        self.lock = RLock()

    def affirm(self, ip: str, t: int, max_visit_times: int):
        if max_visit_times == 0 or t == 0:
            return None, True

        with self.lock:
            v = self.visit_map.get(ip)
            if v is None:
                self.visit_map[ip] = Visiter()
            else:
                if time.time() - v.last_visit > t:
                    v.visit_times = 1
                elif v.visit_times > max_visit_times:
                    return v, False
                else:
                    v.visit_times += 1
                v.last_visit = time.time()

        return None, True

    def take_last_visitor(self, ip: str):
        with self.lock:
            v = self.visit_map.get(ip)
            if v:
                return v.last_visit
            return None

    def take_visit_times(self, ip: str):
        with self.lock:
            v = self.visit_map.get(ip)
            if v:
                return v.visit_times
            return 0
