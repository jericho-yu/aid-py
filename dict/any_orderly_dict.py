from typing import Any, Dict, List, Optional
from threading import RLock


def new_orderly_dict(key: Any, value: Any) -> "OrderlyDict":
    return OrderlyDict(key, value)


def new_any_orderly_dict(
    m: Optional[Dict[Any, Any]] = None, keys: List[Any] = None
) -> "AnyOrderlyDict":
    return AnyOrderlyDict(m, keys)


class OrderlyDict:
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value


class AnyOrderlyDict:
    def __init__(
        self, m: Optional[Dict[Any, Any]] = None, keys: Optional[List[Any]] = None
    ):
        self.data = []
        self.keys = []
        self.lock = RLock()
        if m and keys:
            for key in keys:
                self.data.append(OrderlyDict(key, m[key]))
                self.keys.append(key)

    def set_by_index(self, index: int, key: Any, value: Any):
        with self.lock:
            if index < len(self.data):
                self.data[index] = OrderlyDict(key, value)
            else:
                self.data.append(OrderlyDict(key, value))
            if key not in self.keys:
                self.keys.append(key)

    def set_by_key(self, key: Any, value: Any):
        with self.lock:
            for item in self.data:
                if item.key == key:
                    item.value = value
                    return
            self.data.append(OrderlyDict(key, value))
            self.keys.append(key)

    def get(self, key: Any) -> Optional[Any]:
        with self.lock:
            for item in self.data:
                if item.key == key:
                    return item.value
        return None

    def first(self) -> Optional[OrderlyDict]:
        with self.lock:
            return self.data[0] if self.data else None

    def last(self) -> Optional[OrderlyDict]:
        with self.lock:
            return self.data[-1] if self.data else None

    def keys(self) -> List[Any]:
        with self.lock:
            return self.keys

    def to_map(self) -> Dict[Any, Any]:
        with self.lock:
            return {item.key: item.value for item in self.data}

    def all(self) -> List[OrderlyDict]:
        with self.lock:
            return self.data

    def clean(self):
        with self.lock:
            self.data.clear()
            self.keys.clear()

    def len(self) -> int:
        with self.lock:
            return len(self.data)

    def filter(self, fn):
        with self.lock:
            self.data = [item for item in self.data if fn(item)]

    def copy(self):
        with self.lock:
            return AnyOrderlyDict(self.to_map(), self.keys)
