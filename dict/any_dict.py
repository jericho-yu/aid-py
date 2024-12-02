import threading
from collections.abc import dict_keys, dict_values
from typing import Dict, Any, Callable, List


def new(dictionary: Dict[Any, Any]) -> 'AnyDict':
    return AnyDict(dictionary)


class AnyDict:
    def __init__(self, dictionary: Dict[Any, Any]) -> None:
        self.dictionary = dictionary
        self.lock = threading.Lock()

    def set(self, key: Any, value: Any) -> None:
        with self.lock:
            self.dictionary[key] = value

    def get(self, key: Any) -> Any:
        with self.lock:
            return self.dictionary[key]

    def to_dict(self) -> Dict[Any, Any]:
        with self.lock:
            return self.dictionary

    def len(self) -> int:
        with self.lock:
            return len(self.dictionary)

    def filter(self, fn: Callable[[Any], bool]) -> 'AnyDict':
        with self.lock:
            self.dictionary = {k: v for k, v in self.dictionary.items() if fn(v)}

            return self

    def remove_empty(self) -> 'AnyDict':
        with self.lock:
            self.dictionary = {k: v for k, v in self.dictionary.items() if v}

            return self

    def join_without_empty(self, separator: str) -> str:
        with self.lock:
            return separator.join(self.remove_empty().to_dict())

    def get_values(self) -> dict_values[Any, Any]:
        with self.lock:
            return self.dictionary.values()

    def get_keys(self) -> dict_keys[Any, Any]:
        with self.lock:
            return self.dictionary.keys()