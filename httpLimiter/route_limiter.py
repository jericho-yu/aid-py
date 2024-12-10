import time
from threading import RLock
from ip_limiter import IpLimiter


class RouteLimiter:
    def __init__(self):
        self.route_set_map = {}
        self.lock = RLock()

    def give(self, router: str, t: int, max_visit_times: int):
        with self.lock:
            self.route_set_map[router] = {
                "ip_limiter": IpLimiter(),
                "t": t,
                "max_visit_times": max_visit_times,
            }
        return self

    def affirm(self, router: str, ip: str):
        with self.lock:
            if router in self.route_set_map:
                v = self.route_set_map[router]
                return v["ip_limiter"].affirm(ip, v["t"], v["max_visit_times"])
        return None, True
