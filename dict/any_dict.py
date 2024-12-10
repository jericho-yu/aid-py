import threading
from typing import Dict, Any, Callable, List


def new(dictionary: Dict[Any, Any]) -> "AnyDict":
	return AnyDict(dictionary)


class AnyDict:
	def __init__(self, dictionary: Dict[Any, Any]) -> None:
		self.dictionary = dictionary
		self.lock = threading.Lock()

	def copy(self) -> "AnyDict":
		"""
		复制
		:return: AnyDict
		"""
		with self.lock:
			return AnyDict(self.dictionary.copy())

	def set(self, key: Any, value: Any) -> "AnyDict":
		"""
		设置值
		:param key: Any
		:param value: Any
		:return: AnyDict
		"""
		with self.lock:
			self.dictionary[key] = value

			return self

	def take(self, key: Any) -> Any:
		"""
		获取值
		:param key: Any
		:return: Any
		"""
		with self.lock:
			return self.dictionary[key]

	def to_dict(self) -> Dict[Any, Any]:
		"""
		转字典
		:return:
		"""
		with self.lock:
			return self.dictionary

	def length(self) -> int:
		"""
		获取字典长度
		:return:
		"""
		with self.lock:
			return len(self.dictionary)

	def filter(self, fn: Callable[[Any], bool]) -> "AnyDict":
		"""
		过滤
		:param fn: Callable[[Any],bool]
		:return: AnyDict
		"""
		with self.lock:
			self.dictionary = {k: v for k, v in self.dictionary.items() if fn(v)}

			return self

	def remove_empty(self) -> "AnyDict":
		""" "
		去掉空值
		:return: AnyDict
		"""
		with self.lock:
			self.dictionary = {k: v for k, v in self.dictionary.items() if v}

			return self

	def join_without_empty(self, sep: str) -> str:
		"""
		连接字符串
		:param sep: str
		:return: str
		"""
		with self.lock:
			return sep.join(self.copy().remove_empty().to_dict())

	def take_values(self) -> List[Any]:
		"""
		获取所有的值
		:return:
		"""
		with self.lock:
			return [v for _, v in self.dictionary.items()]

	def take_keys(self) -> List[Any]:
		"""
		获取所有的键
		:return: List[Any]
		"""
		with self.lock:
			return [k for k in self.dictionary]

	def has_key(self, key: Any) -> bool:
		"""
		检查键是否存在
		:param key: Any
		:return: bool
		"""
		with self.lock:
			return key in [k for k in self.dictionary.items()]

	def has_value(self, value: Any) -> bool:
		"""
		检查值是否存在
		:param value: Any
		:return: bool
		"""
		with self.lock:
			return value in [v for _, v in self.dictionary.items()]

	def all(self) -> bool:
		"""
		检查是否全部都是空值
		:return: bool
		"""
		with self.lock:
			return all([v for _, v in self.dictionary.items() if v])

	def any(self) -> bool:
		"""
		检查是否存在任意值
		:return: bool
		"""
		with self.lock:
			return any([v for _, v in self.dictionary.items() if v])

	def take_keys_by_value(self, value: Any) -> List[Any]:
		"""
		通过值获取键
		:param value: Any
		:return: List[Any]
		"""
		with self.lock:
			return [k for k, v in self.dictionary.items() if v == value]

	def destroy_by_key(self, key: Any) -> "AnyDict":
		"""
		通过键删除
		:param key: Any
		:return: AnyDict
		"""
		with self.lock:
			self.dictionary.pop(key)
			return self

	def destroy_by_keys(self, keys: List[Any]) -> "AnyDict":
		"""
		通过键删除
		:param keys: List[Any]
		:return: AnyDict
		"""
		with self.lock:
			for key in keys:
				self.dictionary.pop(key)
			return self

	def destroy_by_value(self, value: List[Any]) -> "AnyDict":
		"""
		通过值删除
		:param value: List[Any]
		:return: AnyDict
		"""
		with self.lock:
			for k, v in self.dictionary.items():
				if v == value:
					self.dictionary.pop(k)
				return self
	
	def destroy_by_values(self, values: List[Any]) -> "AnyDict":
		"""
		通过值删除
		:param values: List[Any]
		:return: AnyDict
		"""
		with self.lock:
			for k, v in self.dictionary.items():
				if v in values:
					self.dictionary.pop(k)
				return self

	def clean(self) -> "AnyDict":
		"""
		清空字典
		:return: AnyDict
		"""
		with self.lock:
			self.dictionary.clear()
			return self