import threading
import time

class ItemLock:
    def __init__(self, val, timeout=0):
        self.in_use = False
        self.val = val
        self.timeout = timeout
        self.timer = None

    def release(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
        self.in_use = False

class MapLock:
    def __init__(self):
        self.locks = {}
        self.lock = threading.RLock()

    def give(self, key, val):
        with self.lock:
            if key in self.locks:
                raise ValueError(f"Lock [{key}] already exists")
            self.locks[key] = ItemLock(val)

    def give_many(self, items):
        with self.lock:
            for key, val in items.items():
                self.give(key, val)

    def destroy(self, key):
        with self.lock:
            if key in self.locks:
                self.locks[key].release()
                del self.locks[key]

    def destroy_all(self):
        with self.lock:
            for key in list(self.locks.keys()):
                self.destroy(key)

    def lock(self, key, timeout=0):
        with self.lock:
            if key not in self.locks:
                raise ValueError(f"Lock [{key}] does not exist")
            item = self.locks[key]
            if item.in_use:
                raise ValueError(f"Lock [{key}] is in use")
            item.in_use = True
            if timeout > 0:
                item.timeout = timeout
                item.timer = threading.Timer(timeout, self._release_lock, args=[key])
                item.timer.start()
            return item

    def try_lock(self, key):
        with self.lock:
            if key not in self.locks:
                raise ValueError(f"Lock [{key}] does not exist")
            item = self.locks[key]
            if item.in_use:
                raise ValueError(f"Lock [{key}] is in use")
            return True

    def _release_lock(self, key):
        with self.lock:
            if key in self.locks:
                self.locks[key].release()

    def demo(self):
        k8s_links = {
            "k8s-a": {},
            "k8s-b": {},
            "k8s-c": {}
        }

        self.give_many(k8s_links)

        try:
            self.try_lock("k8s-a")
        except ValueError as e:
            print(e)

        try:
            lock = self.lock("k8s-a", 10)
            time.sleep(5)
            lock.release()
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    map_lock = MapLock()
    map_lock.demo()